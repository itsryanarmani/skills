#!/usr/bin/env bash
# Use a cloned voice once more. An ID that no speech call has used is deleted after 7 days;
# one call makes it reusable. This is cheap insurance, not a proven requirement.
#
#   keepalive.sh VOICE_ID        # costs about $0.002
set -euo pipefail
exec </dev/null
id="$1"
[[ -n "${WAVESPEED_API_KEY:-}" ]] || { echo "set WAVESPEED_API_KEY first" >&2; exit 2; }
wavespeed run minimax/speech-02-hd -i voice_id="$id" -i text="Checking in." --json >/dev/null
f="${VOICE_DIR:-$HOME/.voice-clones}/$id/voice.json"
[[ -f "$f" ]] && python3 -I - "$f" <<'PY'
import datetime, json, sys
v = json.load(open(sys.argv[1])); v["last_used"] = datetime.date.today().isoformat()
json.dump(v, open(sys.argv[1], "w"), indent=2)
PY
echo "kept alive $id on $(date -u +%F)"
