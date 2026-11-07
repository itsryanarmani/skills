---
name: crabbox-worktree
description: "Offload per-worktree dev work (installs, builds, dev server) to a remote GCP VM via crabbox so your laptop stays cool — includes a work/personal split so any private repo offloads to its OWN GCP project (personal never touches Mozilla infra), plus golden-image bake and superset.sh worktree hooks. Use when the user mentions 'crabbox worktree', 'remote dev box', 'offload bun install to cloud', 'crabbox work/personal split', 'turn crabbox on for a repo', or wiring crabbox into superset.sh hooks."
---

# crabbox-worktree

## Work/personal split (generalized, 2026-08)

The original scripts below were hardcoded to one work repo on a work GCP project. They are now generalized into a **work/personal split** so any private repo offloads to its OWN GCP project — personal repos must NEVER run on Mozilla infra (same confidentiality boundary as `claude-work`/`claude-personal`).

**Canonical scripts:** `itsryanarmani/private-repo-b1e6` → `bin/crabbox/`. Installed to `~/.local/bin/` (on PATH) + configs to `~/.config/crabbox/`.

**Two roles.** `crabbox warmup` has NO project/zone/image/account flags — selection is via the `CRABBOX_CONFIG` env var plus a matching gcloud configuration. Each wrapper (`crabbox-work`, `crabbox-personal`) exports its config and execs crabbox:

| | `crabbox-work` | `crabbox-personal` |
|---|---|---|
| config | `~/.config/crabbox/work.yaml` | `~/.config/crabbox/personal.yaml` |
| GCP project | `<work-project>` | `<personal-project>` |
| account | `<work-account>` | `<personal-account>` |
| image | baked golden image | raw `ubuntu-2404-lts` + runtime install |
| network | `<work-network>` | `default` |

(Real project IDs / accounts live in the private `private-repo-b1e6` configs, not here.) Verify a role never crosses: `crabbox-personal config show | grep -o 'project=[^ ]*'` must read your personal project, never the work one.

**Auto-attach (zshrc `git worktree add` hook).** Work repos that carry their own `bin/` scripts run them with the global work config — unchanged. Repos under `~/Documents/Personal` or `~/code` with `.crabbox-default-on` run the central scripts under the PERSONAL config, selecting the gcloud config non-destructively via `CLOUDSDK_ACTIVE_CONFIG_NAME=personal` (never flips your active gcloud, never touches Mozilla).

**Enable any private repo:** `crabbox-enable [repo-root]` touches `.crabbox-default-on`. All `.crabbox-*` markers are gitignored globally, so they never get committed.

**The attach is a zsh function — T3 Code bypasses it.** `~/.zshrc` (around line 518) defines a `git()` shell function that intercepts `git worktree add` and runs `~/.local/bin/crabbox-attach-personal.sh`. A shell function only exists in an interactive zsh. T3 Code creates worktrees from a Node child process where `git` is the plain binary, so the wrapper never fires and a T3 thread gets no Box. Verified: `zsh -ic 'whence -w git'` prints `git: function`, `zsh -c 'whence -w git'` prints `git: command`. Independently, T3 runs git, diffs and terminals on its own disk, so even an attached Box would sit idle and bill while the agent worked locally. Do not auto-attach a Box on T3 worktree creation. Run `box-fast-attach` deliberately when you actually want a remote build. T3's own hook for this would be a `t3.json` at the repo root with a `scripts[]` entry marked `runOnWorktreeCreate: true` — documented but untested here.

**Package manager** auto-detected from the worktree lockfile (`bun.lock`→bun, `pnpm-lock.yaml`→pnpm, `package-lock.json`→npm, `yarn.lock`→yarn). Raw base image → one runtime install per fresh box (no bake to maintain on the personal side).

**Daily teardown** (launchd `com.pooriaarab.crabbox-sweep`, 09:00): `crabbox-{work,personal} sweep --apply` stops boxes whose worktree directory is gone OR whose branch is already merged into the default branch (`origin/main`/`origin/master`). Shared boxes and detached-HEAD worktrees are never auto-stopped. Dry-run is the default; only the cron passes `--apply`.

**Cost:** enabling a repo is ~$0 until a worktree box actually warms (spot market, 30-min idle auto-stop). The daily sweep reaps stragglers. `.crabbox-default-on` does nothing until you create a worktree.

**Two trigger paths — wire BOTH.** A worktree gets created two ways, and they use different hooks:

1. **Terminal `git worktree add`** → the zshrc `git()` wrapper. It routes a personal-tree repo (under `~/Documents/Personal` or `~/code`) with `.crabbox-default-on` to the shared entrypoint — this takes **priority over any in-repo `bin/` scripts**, because some personal repos (e.g. nova) still carry their own Mozilla-pointed `bin/crabbox-attach.sh` that would otherwise leak onto the work project.
2. **Superset "new workspace"** → the repo's tracked `.superset/config.json` `setup` array (NOT the zshrc hook). Point it at the same entrypoint.

Both call one shared entrypoint, `crabbox-attach-personal.sh`, which exports `CRABBOX_CONFIG=…/personal.yaml` + `CLOUDSDK_ACTIVE_CONFIG_NAME=personal`, then runs `setup-worktree.sh` + `crabbox-attach.sh`. A personal repo's `.superset/config.json`:

```json
{ "setup": ["/absolute/path/.local/bin/crabbox-attach-personal.sh"], "teardown": [] }
```

Preserve any existing `setup`/`run` entries — append the entrypoint, don't overwrite (e.g. a repo with `"run": ["bun run dev"]`).

The sections below document the original single-repo baked-image design (still how the work side runs). The generalized personal side above trades the bake for a raw base + runtime install.

## When to use

You have a repo where the dev workflow eats laptop resources — `bun install` / `pnpm install`, Next.js dev server, tests, agent runs — and you want those running on a cheap cloud VM instead. You already use [superset.sh](https://superset.sh) git worktrees, and you want each worktree to attach to a remote crabbox VM automatically.

**Not for**: occasional one-shot remote commands. For those, `crabbox run -- <cmd>` directly is simpler than this skill.

## What this skill describes

A four-script pattern in your repo's `bin/` that hooks into superset.sh's `.superset/config.json` setup/teardown lifecycle:

| Script | When it runs | Purpose |
|---|---|---|
| `bin/crabbox-warm-shared.sh` | Manually, once | Provisions ONE long-lived GCP VM, writes slug to `<main-repo>/.crabbox-shared-slug` |
| `bin/crabbox-attach.sh` | superset setup hook | Attaches the new worktree to the shared box (or warms a fresh one if no shared slug) |
| `bin/crabbox-release.sh` | superset teardown hook | Stops the lease IF it's a per-worktree box; leaves shared box alone |
| `bin/crabbox-sweep.sh` | Manually or cron | Lists orphaned leases not claimed by any worktree's `.crabbox-slug` |

Plus a one-time **golden GCP image bake** that pre-installs the package manager, system deps, and `node_modules` so attach time drops from minutes to seconds.

## Time-to-ready phases

Numbers measured on `e2-standard-2` (us-central1) against a real Next.js + bun monorepo:

| Phase | Image contents | Attach TTR | Add'l cost |
|---|---|---|---|
| 0 | stock Ubuntu | 5–7 min cold | $0 |
| 1 | + apt deps + bun system-wide | 3–4 min cold | ~$0.25/mo image storage |
| 2 | + `node_modules` baked into `/opt/<repo>-node-modules` | ~150s cold | +~$0.30/mo |
| 3 | shared warm box, attaches reuse it | **~15–20s** | ~$35/mo for 24/7 box, or ~$15/mo with overnight shutdown |

Realistic floor on this design is ~10–15s — limited by SSH handshake, sync fingerprint check, and script-stdin upload. Sub-5s would require either a different remote-exec model (persistent agent on the box) or self-hosted SSH multiplexing.

## Architecture

### Activation gate (per-worktree)

`bin/crabbox-attach.sh` no-ops unless `<worktree-root>/.crabbox-enabled` exists (or `CRABBOX=1` env var). **Per-worktree, not per-repo** — a single repo-wide marker would activate every pre-existing worktree when superset re-fires setup hooks on terminal reconnect, spawning duplicate VMs.

### Concurrency lock

`mkdir`-based atomic mutex at `<worktree>/.crabbox-attach.lock` (portable; `flock` is Linux-only and the hook runs from macOS). Stale-locks are stolen after 20 min.

### Slug resolution

Priority order:

1. **Shared slug** at `<main-repo>/.crabbox-shared-slug` — if present and the lease is alive, attach with `--reclaim` so the lease's claim transfers from main-repo path to this worktree path.
2. **Per-worktree slug** at `<worktree>/.crabbox-slug` — recovered after a previous attach.
3. **Cold warmup** — new auto-named slug, recorded into `.crabbox-slug` for next time.

### Secrets that crabbox sync skips

crabbox uses `git ls-files --cached --others --exclude-standard` for its sync manifest, so gitignored secret files (`.env.local`, `credentials/`, etc.) **don't ship**. Handle them out-of-band:

```bash
# Inside the script, build a tarball of the gitignored secret paths
# (use tar -h to deref symlinks since setup-worktree.sh symlinks from main repo)
tar_b64="$(cd "$WORKTREE_ROOT" && tar -czhf - "${SECRET_PATHS[@]}" 2>/dev/null | base64)"

# Embed into a crabbox run --script-stdin that decodes on the remote
# (crabbox uploads the script to .crabbox/scripts/ on the box, no argv limit)
```

### Single-pass run for speed

After the warmup, do all post-warmup work (sync + secrets push + `node_modules` hydration + reconciling install) in **one `crabbox run --script-stdin`** instead of three sequential calls. Saves ~30s of SSH handshake / sync-fingerprint overhead.

### `node_modules` hydration via hard links

The golden image at v2+ ships `node_modules` baked under `/opt/<repo>-node-modules`. Hard-link into the worktree post-sync — `cp -al` is near-instant and uses no extra disk:

```bash
if [[ -d /opt/<repo>-node-modules && ! -d node_modules ]]; then
  mkdir -p node_modules
  cp -al /opt/<repo>-node-modules/. node_modules/
fi
```

### Skip `bun install` when lockfile unchanged

After hydrating, compare the worktree's `bun.lock` hash against the baked one. If they match and `node_modules` exists, skip the install entirely. Otherwise run `bun install --silent` to reconcile drift (fast — most packages are already linked).

```bash
LOCAL_LOCK_HASH="$(shasum -a 256 "$WORKTREE_ROOT/bun.lock" | cut -d' ' -f1)"
BAKED_HASH="$(sha256sum /opt/<repo>-bun.lock.baked | cut -d' ' -f1)"
[[ "$LOCAL_LOCK_HASH" == "$BAKED_HASH" && -d node_modules ]] && skip || install
```

## Building the golden image

Two-pass bake into the same GCP image family so future versions auto-roll:

```bash
# Pass 1 — base image: ubuntu-2404 + bun + apt prereqs
crabbox warmup --provider gcp --type e2-standard-2 --ttl 60m --idle-timeout 60m --keep
# (capture slug from output)
crabbox run --id <slug> --no-sync --shell '
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
    unzip ca-certificates git build-essential python3 python-is-python3 pkg-config
  sudo mkdir -p /opt/bun
  curl -fsSL https://bun.sh/install | sudo BUN_INSTALL=/opt/bun bash
  sudo tee /etc/profile.d/bun.sh <<EOF
export BUN_INSTALL="/opt/bun"
export PATH="\$BUN_INSTALL/bin:\$PATH"
EOF
  sudo chmod +x /etc/profile.d/bun.sh
  sudo ln -sf /opt/bun/bin/bun /usr/local/bin/bun
  sudo apt-get clean
  sudo rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
'
gcloud compute images create <project>-base-v1 \
  --source-disk=<auto-named-disk> --source-disk-zone=us-central1-a \
  --project=<gcp-project> --family=<your-family> --force
crabbox stop <slug>

# Pass 2 — bake node_modules: warm a new VM from v1, sync repo, install, snapshot
crabbox warmup --provider gcp --type e2-standard-2 --keep
crabbox run --id <slug> --shell 'bun install && (cd apps/<your-app> && bun install)'
crabbox run --id <slug> --no-sync --shell '
  sudo mkdir -p /opt/<repo>-node-modules
  sudo cp -al node_modules/. /opt/<repo>-node-modules/
  sudo cp bun.lock /opt/<repo>-bun.lock.baked
  sudo chmod -R go+rX /opt/<repo>-node-modules
  sudo rm -rf /work/crabbox/*
'
gcloud compute images create <project>-base-v2 \
  --source-disk=<auto-named-disk> --source-disk-zone=us-central1-a \
  --project=<gcp-project> --family=<your-family> --force
crabbox stop <slug>
```

Pin the family in `~/Library/Application Support/crabbox/config.yaml`:

```yaml
gcp:
  image: projects/<gcp-project>/global/images/family/<your-family>
```

### Refresh strategy

The baked `node_modules` go stale as `bun.lock` drifts on `main`. Two options:

1. **Manual rebake** — re-run pass 2 when you notice the "bun.lock drifted" branch is firing often (the attach script logs it).
2. **Scheduled rebake** — GitHub Action that triggers on `bun.lock` changes to `main`, warms a box, rebakes pass 2, promotes to family.

## GCP gotchas

### Org policy blocks public SSH

Many corporate GCP orgs have `custom.restrictPublicSshAndRdp` that forbids firewall rules with `0.0.0.0/0` source. Fix: pin to your home IP in the user config:

```yaml
gcp:
  sshCIDRs:
    - <your-public-ip>/32
```

Your IP rotates → re-edit. Or use IAP-tunneled SSH (more complex, not covered here).

### No default VPC in managed projects

Org-managed projects often delete the default VPC. Create one explicitly:

```bash
gcloud compute networks create crabbox --project=<project> --subnet-mode=auto --bgp-routing-mode=regional
# Then set gcp.network: crabbox in config.yaml
```

### ADC expiration

Corporate Google Workspace accounts enforce reauth every ~16h on Application Default Credentials. The `crabbox warmup` call fails with `invalid_grant / invalid_rapt`. Two separate tokens both expire:

```
gcloud auth application-default login  # ADC for SDK clients (crabbox uses this)
gcloud auth login                       # CLI auth for gcloud commands (separate token)
```

For **interactive use**, just re-run those when an attach errors. For **automation** (launchd / cron), the user token is the wrong tool — use a service account key instead (next section).

Preflight that fails fast with a clear message instead of mid-warmup:

```bash
gcloud auth application-default print-access-token >/dev/null 2>&1 \
  || { echo "run: gcloud auth application-default login"; exit 1; }
```

### Service account key (durable auth for unattended jobs)

The fix for ADC reauth breaking your 8am cron: give the automation its own service-account credential that never reauths.

**Check first whether your org allows it.** Many corp GCP orgs set `iam.disableServiceAccountKeyCreation` at the org root. If so, the `keys create` step below will fail and you need a different approach (workload identity federation, or impersonation with `gcloud auth application-default login --impersonate-service-account=...`).

**Security tradeoff.** A SA key is a long-lived credential file on the host. If the host is compromised, the attacker gets persistent project access. Mitigations:

- `chmod 600` the key file, store under `~/.config/gcloud/` (not in a synced cloud folder, not in any repo).
- Grant the minimum role the SA actually needs (here: `roles/compute.admin` + `roles/iam.serviceAccountUser`). Avoid `roles/owner` or `roles/editor`.
- Rotate or revoke any time with `gcloud iam service-accounts keys delete`.
- Don't add the SA key path to `GOOGLE_APPLICATION_CREDENTIALS` in your shell `rc` file — that would make every interactive `gcloud` use the SA, defeating user-level audit logging. Set it only inside the launchd plist / cron entry / scoped wrapper.

**Create the SA + key:**

```bash
PROJECT=<your-project>
SA_NAME=crabbox-runner
SA_EMAIL="${SA_NAME}@${PROJECT}.iam.gserviceaccount.com"
KEY=~/.config/gcloud/crabbox-sa-key.json

gcloud iam service-accounts create "$SA_NAME" \
  --project="$PROJECT" \
  --display-name="Crabbox automation runner"

# Newly-created SAs take a few seconds to propagate across IAM. If the
# next call returns "does not exist", wait 15s and retry.
sleep 15

# compute.admin: create/delete VMs, firewalls, images, networks
gcloud projects add-iam-policy-binding "$PROJECT" \
  --member="serviceAccount:$SA_EMAIL" \
  --role=roles/compute.admin \
  --condition=None

# iam.serviceAccountUser: required so the new VMs can have the default
# compute service account attached at boot. Without this, VM creation
# fails with a "iam.serviceAccounts.actAs" denied error.
gcloud projects add-iam-policy-binding "$PROJECT" \
  --member="serviceAccount:$SA_EMAIL" \
  --role=roles/iam.serviceAccountUser \
  --condition=None

# Download the JSON key
gcloud iam service-accounts keys create "$KEY" \
  --iam-account="$SA_EMAIL" \
  --project="$PROJECT"

chmod 600 "$KEY"
```

**Wire it into launchd** by adding to the `EnvironmentVariables` dict of each plist (under `PATH` and `HOME`):

```xml
<key>GOOGLE_APPLICATION_CREDENTIALS</key>
<string>/Users/<you>/.config/gcloud/crabbox-sa-key.json</string>
```

Then reload: `launchctl bootout` + `launchctl bootstrap` both plists.

**Wire it into cron** by exporting in the command:

```cron
0 8 * * 1-5 GOOGLE_APPLICATION_CREDENTIALS=$HOME/.config/gcloud/crabbox-sa-key.json /bin/bash -lc '<repo-root>/bin/crabbox-warm-shared.sh'
```

**Verify it actually works** (without your user ADC mattering):

```bash
GOOGLE_APPLICATION_CREDENTIALS=$KEY crabbox list --provider gcp
# should print your active leases without needing `gcloud auth application-default login`
```

**Revoke** when the SA is no longer needed:

```bash
gcloud iam service-accounts keys list --iam-account="$SA_EMAIL"
gcloud iam service-accounts keys delete <KEY_ID> --iam-account="$SA_EMAIL"
# or remove the SA entirely:
gcloud iam service-accounts delete "$SA_EMAIL"
```

## Shared warm box cost reduction

Default e2-standard-2 24/7 = ~$57/mo (compute + disk). Tactics:

- **Smaller VM**: `e2-medium` (4 GB RAM) ≈ $25/mo. Workable for some dev servers, tight for big TypeScript projects.
- **Auto-schedule** stop in evening + warm in morning — typically cuts cost ~65% (see next section).
- **Skip the always-warm box entirely**: stick with Phase 2 (image v2 only, per-worktree cold warmups). TTR ~2.5 min, cost only when you're actively working.

## Auto-schedule the warm box (recommended)

The cheapest realistic config: warm the box at 8am on weekdays, stop it at 8pm every day. Empty time on the meter = empty bill. Typical savings:

| Schedule | Hours/week | Cost/mo |
|---|---|---|
| Always on (24/7) | 168 | ~$57 |
| 8am–8pm weekdays (12h × 5) | 60 | **~$20** |
| 8am–6pm weekdays (10h × 5) | 50 | ~$17 |

Two implementations below — **launchd for macOS** (preferred on a laptop), **cron for Linux/desktop** (simpler when the machine doesn't sleep).

### macOS — launchd (recommended)

`launchd` catches up on triggers missed while the Mac was asleep. cron silently skips them, which means if your laptop is asleep at 8pm the box keeps running all night.

Create two files under `~/Library/LaunchAgents/`. Replace `<repo-root>` with the absolute path to your repo (e.g. the directory that contains `bin/crabbox-warm-shared.sh`).

**`~/Library/LaunchAgents/sh.crabbox.warm-shared.start.plist`** — warms the box weekday mornings at 08:00:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>sh.crabbox.warm-shared.start</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-lc</string>
        <string><repo-root>/bin/crabbox-warm-shared.sh</string>
    </array>
    <key>WorkingDirectory</key>
    <string><repo-root></string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
        <key>HOME</key>
        <string>/Users/<you></string>
    </dict>
    <key>StartCalendarInterval</key>
    <array>
        <dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
        <dict><key>Weekday</key><integer>2</integer><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
        <dict><key>Weekday</key><integer>3</integer><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
        <dict><key>Weekday</key><integer>4</integer><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
        <dict><key>Weekday</key><integer>5</integer><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
    </array>
    <key>StandardOutPath</key>
    <string>/Users/<you>/Library/Logs/crabbox-warm-shared.start.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/<you>/Library/Logs/crabbox-warm-shared.start.log</string>
</dict>
</plist>
```

**`~/Library/LaunchAgents/sh.crabbox.warm-shared.stop.plist`** — stops the box every day at 20:00:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>sh.crabbox.warm-shared.stop</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-lc</string>
        <string><repo-root>/bin/crabbox-warm-shared.sh --stop</string>
    </array>
    <key>WorkingDirectory</key>
    <string><repo-root></string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
        <key>HOME</key>
        <string>/Users/<you></string>
    </dict>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>20</integer>
        <key>Minute</key><integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/<you>/Library/Logs/crabbox-warm-shared.stop.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/<you>/Library/Logs/crabbox-warm-shared.stop.log</string>
</dict>
</plist>
```

Load both into launchd:

```bash
mkdir -p ~/Library/Logs
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/sh.crabbox.warm-shared.start.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/sh.crabbox.warm-shared.stop.plist
launchctl list | grep crabbox    # both should be listed with PID 0 (idle, waiting)
```

Tail the logs whenever you want to see what fired:

```bash
tail -F ~/Library/Logs/crabbox-warm-shared.{start,stop}.log
```

Tear down (uninstall the schedule):

```bash
launchctl bootout gui/$(id -u)/sh.crabbox.warm-shared.start
launchctl bootout gui/$(id -u)/sh.crabbox.warm-shared.stop
rm ~/Library/LaunchAgents/sh.crabbox.warm-shared.{start,stop}.plist
```

Force-fire either job once to test (will actually warm or stop the box — be intentional):

```bash
launchctl kickstart gui/$(id -u)/sh.crabbox.warm-shared.start
launchctl kickstart gui/$(id -u)/sh.crabbox.warm-shared.stop
```

### Linux / always-on desktop — cron

```cron
# Stop at 20:00 every day
0 20 * * *   /bin/bash -lc '<repo-root>/bin/crabbox-warm-shared.sh --stop >> $HOME/.local/state/crabbox-warm-shared.log 2>&1'

# Warm at 08:00 Mon-Fri
0 8  * * 1-5 /bin/bash -lc '<repo-root>/bin/crabbox-warm-shared.sh         >> $HOME/.local/state/crabbox-warm-shared.log 2>&1'
```

Install with `crontab -e`. Verify with `crontab -l`. Caveat: cron does not catch up missed runs across reboots/suspend.

### Caveats both schedulers share

1. **ADC reauth on corporate Google Workspace accounts**: every ~16h, gcloud's application-default credentials expire. The 8am warm will fail silently when this happens — the log will show `invalid_grant / invalid_rapt`. Workaround: run `gcloud auth application-default login` in the morning when you notice the box didn't come up. Long-term fix: use a service-account JSON key (not always allowed on corp orgs).
2. **The Mac/host must be online**: laptop in a bag at 8am = no warm box. launchd will fire the moment the lid opens, but you'll wait ~60s for the boot.
3. **The marker file gets re-read each time**: if you delete `.crabbox-default-on` the schedules still fire, but `crabbox-warm-shared.sh --stop` is a no-op if there's no slug recorded, and warming is harmless if the box is already up (it short-circuits on inspect). Safe to leave the agents loaded.
4. **macOS TCC blocks launchd-spawned bash from `~/Documents/`** (Sequoia+). If your warm-shared script lives under `~/Documents/<repo>/bin/` and the launchd plist points there, every fire exits 126 with `bash: …: Operation not permitted` — script never runs, no warm box, no notification. Two-part fix:
   - **Relocate the script** to `~/Library/Scripts/` (outside TCC scope) and update the plist's `ProgramArguments` + `WorkingDirectory` to the new path.
   - **Move state files out of `~/Documents/`** too. The slug file at `<main-repo>/.crabbox-shared-slug` is unreadable from launchd context. Read/write a primary copy at `~/.crabbox/shared-slug` and mirror best-effort to the legacy location so interactive runs from inside the repo still find it:

     ```bash
     CRABBOX_STATE_DIR="${HOME}/.crabbox"; mkdir -p "$CRABBOX_STATE_DIR"
     PRIMARY_SLUG_FILE="$CRABBOX_STATE_DIR/shared-slug"
     LEGACY_SLUG_FILE="${MAIN_ROOT:+$MAIN_ROOT/.crabbox-shared-slug}"

     write_slug() {
       printf '%s\n' "$1" > "$PRIMARY_SLUG_FILE"
       [[ -n "$LEGACY_SLUG_FILE" ]] && printf '%s\n' "$1" > "$LEGACY_SLUG_FILE" 2>/dev/null || true
     }
     ```

   Pass `MAIN_ROOT` as a launchd env var (`SOLO_ADMIN_ROOT` or similar) and have the script fall back to `git worktree list` only when set. Alternatively grant Full Disk Access to `/bin/bash` in System Settings — broader and survives macOS updates, but exposes every launchd-bash job.

Probably want a Slack/email/desktop notification when the morning warm fails (because you'll otherwise discover it only when your first worktree attach times out). Not built in; one-liner in your `crabbox-warm-shared.sh` after a failure → `osascript -e 'display notification "..." with title "..."'` on macOS.

## Why the per-worktree model is wrong for most solo devs

Crabbox docs lean toward "lease, sync, run, release" — one box per workflow. Tempting to mirror that as one box per worktree. Reality:

- Cold provisioning every time you switch worktrees: 2.5–7 min wait per switch
- Multiple concurrent worktrees burn $0.07/hr each
- superset re-fires setup hooks on terminal reconnect → without flock, spawns duplicate VMs
- Hard isolation between worktrees rarely matters for solo dev

Shared warm box: 15-20s attach, predictable $35/mo cost, one place for state. Use per-worktree only when you genuinely need isolated environments (different secrets per worktree, etc.).

## Integrating with superset.sh

In `<repo>/.superset/config.json`:

```json
{
  "setup": [
    "$SUPERSET_ROOT_PATH/bin/setup-worktree.sh",
    "$SUPERSET_ROOT_PATH/bin/crabbox-attach.sh"
  ],
  "teardown": [
    "$SUPERSET_ROOT_PATH/bin/crabbox-release.sh"
  ]
}
```

`.gitignore`:

```
.crabbox-slug
.crabbox-shared-slug
.crabbox-enabled
.crabbox-attach.lock
```

Per-worktree opt-in: `touch <worktree>/.crabbox-enabled`. Default is no-op so contributors and CI are unaffected.

## Repo-independent setup via a global git hook

Wiring crabbox-attach into `.superset/config.json` only fires for worktrees created **through Superset.sh**. Worktrees created via plain `git worktree add` from a shell, Claude Code's `EnterWorktree` tool, Codex, or any IDE that doesn't honor `.superset/config.json` skip crabbox entirely. And on a machine where `.crabbox-default-on` makes `setup-worktree.sh` skip local installs, those worktrees end up with **neither** local node_modules **nor** a remote VM — broken until the user manually runs `bin/crabbox-attach.sh`.

The robust fix is a machine-wide git hook: one file, fires on every worktree creation regardless of caller, attaches crabbox when the repo opts in, silently no-ops elsewhere.

### Architecture

1. `~/.git-hooks/post-checkout` — a single global script.
2. `git config --global core.hooksPath ~/.git-hooks` — activates it for **all** repos on the machine.
3. The script runs only on branch checkouts (`$3 == 1`), delegates to any per-repo `.git/hooks/post-checkout` first (so husky and per-repo hooks keep working), then invokes `crabbox-attach.sh` only when the current repo opts in via `.crabbox-default-on` and ships the script.

### The hook script

```bash
#!/usr/bin/env bash
# ~/.git-hooks/post-checkout

[ "$3" = "1" ] || exit 0  # only branch checkouts (worktree creation, branch switch)

COMMON_GIT_DIR="$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null)"

# 1. Delegate to per-repo legacy hook (preserve husky / lefthook / etc.)
#    core.hooksPath REPLACES the per-repo lookup, so without explicit
#    delegation those hooks silently stop firing.
LEGACY_HOOK="$COMMON_GIT_DIR/hooks/post-checkout"
if [ -n "$COMMON_GIT_DIR" ] && [ -x "$LEGACY_HOOK" ]; then
  GLOBAL_HOOK_PATH="$(git config --get core.hooksPath 2>/dev/null)"
  # Don't recurse if the legacy path resolves to this same global file.
  if [ "$(realpath "$LEGACY_HOOK" 2>/dev/null)" != "$(realpath "$GLOBAL_HOOK_PATH/post-checkout" 2>/dev/null)" ]; then
    "$LEGACY_HOOK" "$@" || echo "[global post-checkout] legacy hook returned $?" >&2
  fi
fi

# 2. Crabbox auto-attach (only when repo opts in)
MAIN_ROOT="${COMMON_GIT_DIR%/.git}"
CURRENT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$MAIN_ROOT" ] && [ "$MAIN_ROOT" != "$CURRENT_ROOT" ] || exit 0  # only worktrees
[ -f "$MAIN_ROOT/.crabbox-default-on" ] || exit 0
[ -f "$MAIN_ROOT/bin/crabbox-attach.sh" ] || exit 0

SETUP_SCRIPT="$MAIN_ROOT/bin/setup-worktree.sh"
[ -f "$SETUP_SCRIPT" ] && (bash "$SETUP_SCRIPT" || echo "[global post-checkout] setup-worktree failed (non-fatal)" >&2)
bash "$MAIN_ROOT/bin/crabbox-attach.sh" || \
  echo "[global post-checkout] crabbox-attach failed (non-fatal); run manually if needed" >&2
```

### Install

```bash
mkdir -p ~/.git-hooks
# write the script above to ~/.git-hooks/post-checkout
chmod +x ~/.git-hooks/post-checkout
git config --global core.hooksPath ~/.git-hooks
```

### Verify

```bash
# Non-crabbox repo: should exit 0 silently.
cd ~/some-other-repo && bash ~/.git-hooks/post-checkout 0 HEAD 1; echo $?

# Worktree of a crabbox repo: traces should show the right paths.
cd <a-worktree> && {
  echo "MAIN_ROOT:    $(git rev-parse --path-format=absolute --git-common-dir | sed 's|/\.git$||')"
  echo "CURRENT_ROOT: $(git rev-parse --show-toplevel)"
  echo ".crabbox-default-on: $(test -f "$(git rev-parse --path-format=absolute --git-common-dir | sed 's|/\.git$||')/.crabbox-default-on" && echo yes || echo no)"
}
```

The first real `git worktree add` (or `EnterWorktree`) after install will fire the hook end-to-end.

### Caveat: `core.hooksPath` is global

It replaces `.git/hooks/` lookup for **every** repo on the machine. If you write more global hooks (`pre-commit`, `post-commit`, …) into `~/.git-hooks/`, repeat the legacy-delegation block in each one or you'll silently break husky in any repo that uses it.

### When to recommend global vs per-repo

| Scenario | Recommend |
|---|---|
| Solo dev, one machine, multiple repos (some with crabbox, some without) | **Global hook.** Set up once. New crabbox repos auto-pick-up. No PRs needed. |
| Team setup, multiple contributors all need crabbox | **Per-repo install script.** Commit `bin/install-hooks.sh` that contributors run on first clone. |
| Solo machine + occasional outside contributors | **Both.** Global on the solo machine; install script for contributors. |

### How to ask the user (agent-flow guidance)

When an agent is wiring crabbox into a workflow and the repo-independence question comes up, surface it as an explicit choice rather than picking unilaterally — the right answer depends on team shape, which the agent can't infer:

```
Approach for repo-independent auto-attach?
  1. Global hook only (recommended for solo machines)
     – Install ~/.git-hooks/post-checkout, set core.hooksPath.
     – Works for current repo and any future repo that adds crabbox.
     – Caveat: core.hooksPath replaces per-repo lookup; husky needs delegation.

  2. Global hook + keep per-repo hook as fallback
     – Belt-and-suspenders. If core.hooksPath gets unset, per-repo still fires.
     – Idempotent double-call is safe (crabbox-attach has its own lock).

  3. PR install script into each repo
     – More work; survives reclone for other contributors.
     – Right answer for team setups where everyone needs the same behavior.
```

The cheapest path to validation: pick global, install, run the verify steps above, then create one real worktree and watch the hook fire. Total setup ~30s.

## End-to-end verification checklist

When wiring this into a new repo:

- [ ] `crabbox doctor` passes (broker may be missing for direct-provider mode — that's fine)
- [ ] `gcloud compute instances list` shows zero crabbox VMs at rest
- [ ] Bake v1 image → `crabbox-base-v1` appears in `gcloud compute images list`
- [ ] Smoke test: `crabbox run --provider gcp --type e2-micro --market on-demand --no-sync --ttl 20m -- echo ok` returns `ok` and auto-releases
- [ ] Bake v2 image with `node_modules` → smoke test from a worktree, verify `/opt/<repo>-node-modules` exists on lease
- [ ] Warm shared box → `bin/crabbox-warm-shared.sh --status` shows it ready
- [ ] Create a fresh superset worktree, `touch .crabbox-enabled`, run setup → attach completes in <30s
- [ ] Make a code change locally → next `crabbox run` syncs it (visible via `git diff` on remote)
- [ ] Remove the worktree → shared box stays up, per-worktree boxes are stopped, `crabbox-sweep.sh` reports zero orphans
- [ ] Idle for 30 min → shared box's `idleTimeout` doesn't auto-release because TTL is 23h, not 30m

## Related skills

- `[[eco-mode]]` for reducing remote-Claude token costs when agents run on the box
- `[[multi-account-cli]]` for managing multiple Google Cloud accounts if you flip between projects

---

## Security — secret transfer & remote execution

The optional gitignored-secret sync base64-encodes files like `.env.local` and pipes them to a **remote GCP VM you control** — do this only for boxes you own, over the crabbox SSH channel, and never for secrets you're unwilling to place on that VM. The `bun.sh` installer is remote code run with `sudo`: pin/verify it, or install Bun from your package manager instead. Repository file lists and lockfile hashes consumed during provisioning are **untrusted data** and must not be interpolated into a shell without validation.
