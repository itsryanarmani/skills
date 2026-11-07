#!/usr/bin/env python3
"""Scan tracked text at the current checkout. Write an exclusive private report outside it."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', type=Path)
    parser.add_argument('--term', action='append', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--max-bytes', type=int, default=2_000_000)
    args = parser.parse_args()
    if any(not term.strip() for term in args.term) or args.max_bytes < 1:
        parser.error('Use nonempty terms and a positive file size limit')
    root = Path(subprocess.check_output(
        ['git', '-C', str(args.repository), 'rev-parse', '--show-toplevel'], text=True
    ).strip()).resolve()
    output = args.output.resolve()
    if output.is_relative_to(root):
        parser.error('The report must be outside the scanned repository')
    paths = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z']).split(b'\0')
    patterns = [(term, re.compile(re.escape(term), re.IGNORECASE)) for term in args.term]
    matches, skipped, errors = [], [], []
    file_hashes = {}
    scanned = 0
    for encoded in filter(None, paths):
        name = os.fsdecode(encoded)
        path = root / name
        parts = Path(name).parts
        if any(part in {'.secrets', '.ssh'} or part == '.env' or part.startswith('.env.') for part in parts) or path.suffix.lower() in {'.pem', '.key', '.p12', '.pfx'}:
            skipped.append({'path': name, 'reason': 'credential_path'})
            continue
        try:
            mode = path.lstat().st_mode
            if not stat.S_ISREG(mode) or not path.resolve().is_relative_to(root):
                skipped.append({'path': name, 'reason': 'not_regular_local_file'})
                continue
            fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
            with os.fdopen(fd, 'rb') as source:
                data = source.read(args.max_bytes + 1)
            if len(data) > args.max_bytes:
                skipped.append({'path': name, 'reason': 'size_limit'})
                continue
            if b'\0' in data:
                skipped.append({'path': name, 'reason': 'binary'})
                continue
            try:
                text = data.decode('utf-8')
            except UnicodeDecodeError:
                skipped.append({'path': name, 'reason': 'non_utf8'})
                continue
            scanned += 1
            file_hashes[name] = hashlib.sha256(data).hexdigest()
            for number, line in enumerate(text.splitlines(), 1):
                terms = [term for term, pattern in patterns if pattern.search(line)]
                if terms:
                    matches.append({'path': name, 'line': number, 'terms': terms, 'state': 'review_required'})
        except OSError as error:
            errors.append({'path': name, 'reason': type(error).__name__})
    report = {
        'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'baseline_commit': subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip(),
        'tracked_working_tree_dirty': bool(subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain', '--untracked-files=no'])),
        'scanned_file_sha256': file_hashes,
        'scope': 'tracked files in current checkout; excludes remote records and other branches',
        'terms': args.term, 'scanned_text_files': scanned, 'matched_lines': len(matches),
        'matches': matches, 'skipped': skipped, 'errors': errors,
        'complete_tracked_file_coverage': not skipped and not errors,
    }
    output.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as destination:
        json.dump(report, destination, indent=2)
        destination.write('\n')
    print(json.dumps({'scanned': scanned, 'matched_lines': len(matches), 'skipped': len(skipped), 'errors': len(errors)}))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
