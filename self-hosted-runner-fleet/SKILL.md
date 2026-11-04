---
name: self-hosted-runner-fleet
description: "Run GitHub Actions on your own machine, and know when not to. Use when asked to cut Actions minutes or queue time, add a machine to a runner fleet, decide which jobs are safe to move off hosted runners, choose between self-hosted and a managed ephemeral runner, or debug a self-hosted runner whose jobs die, queue forever, or report offline while busy. Covers the Boat JIT pool for private Linux CI, pool costs, and retired desktop troubleshooting on Linux and Windows/WSL2."
---

# Self-hosted runner fleet

Use the Boat JIT pool for private Linux CI. The desktop fleet below is retired.
Read its sections only to maintain a host that needs special hardware or an OS.
Public repos stay on GitHub-hosted runners. A fork PR can run code on a runner.

## Boat JIT runner pool

Use `runs-on: boat` for build, lint, typecheck, test, E2E, deploy and API waits.
Use `runs-on: boat-8` only for a heavy production build. Keep macOS and Windows
jobs on GitHub-hosted images.

Choose one sandbox per job for a first, bounded pilot. Use a JIT pool when
measured demand and start quotas justify reuse. Each Box runs one JIT runner
at a time. A completed runner exits; the next job gets a new JIT config.
The VM and caches persist between jobs. Admit only trusted CI to this pool.
A new runner process does not provide a fresh VM trust boundary.

Before changing capacity or snapshots, read the
[Boat CI qualification rules](../ci-cost-at-agent-scale/boat-ci-qualification.md).
Use the [scripts runbook](https://github.com/pooriaarab/scripts/blob/main/boat-runners.md)
for commands and current implementation gaps. A required safeguard in that
runbook is not proof that the installed pool implements it.

The broker is a Cloudflare Worker. It receives `workflow_job` webhooks and
calls GitHub `generate-jitconfig`. The Box agent requests a config and runs
it. Keep the GitHub token in the broker. Never store it on a Box. Code lives
in `pooriaarab/scripts`: `workers/boat-runners/`, `boat-runner-agent` and
`boat-pool` (work in progress in #508 and #509).

A JIT runner gets ONLY the labels passed to `generate-jitconfig`. It does not
get `self-hosted` by default. Pass `boat` or `boat-8` and use that single label
in `runs-on`. A list such as `[self-hosted, boat]` cannot match this runner.

Declare the labels for actionlint in `.github/actionlint.yaml`:

```yaml
self-hosted-runner:
  labels: [boat, boat-8]
```

Boxes run Ubuntu 24.04 with passwordless sudo, Docker 29, Node 24 and Bun.
Keep `~/.bun`, Playwright browsers and Docker images warm between jobs.
Clean the job workspace and leftover services without deleting those caches.
One job per Box avoids concurrent fixed-port service collisions. Check cleanup
before dispatching the next job. Do not apply disposable-VM disk or swap hacks.

Prices measured 2026-10-11:

| Box | vCPU / RAM | Hourly price | Label |
| --- | --- | --- | --- |
| small | 2 / 4 GB | $0.018 | no fleet label assigned |
| default | 4 / 8 GB | $0.036 | `boat` |
| large | 8 / 16 GB | $0.072 | `boat-8` |

For comparison, Ubicloud standard-2/4/8 costs $0.075/$0.15/$0.30 per hour.
$1 buys 100,000 Box-seconds. An always-on pool bills wall time, including idle
and queue time, not job time. N default Boxes cost N × $0.036 per hour.
Size the pool from peak job demand, queue delay and idle cost. Check memory
limits before a tier drop; a 12 GB Node heap cannot fit on an 8 GB Box.

## Retired desktop procedure

The following sections describe the old persistent desktop fleet. They do not
set job placement for the Boat pool. Use the label and broker procedure above.

Keep host specifics (address, SSH key, account names, service paths) in a private host
overlay, not in this skill and not in a public repo.

## Decide what moves

| Move to the fleet | Keep on hosted runners |
| --- | --- |
| build, lint, typecheck, unit tests, E2E without fixed-port containers | deploy, release, publish, production smoke |
| dry-run / plan / simulation jobs | anything needing a macOS or Windows image |
| AI review jobs whose repository secret already exists | workflows that execute a prompt from comment text |
| formatting bots that push back to a PR branch | jobs uploading SARIF through `gitleaks-action` (see below) |

Two rules worth stating plainly:

- **GitHub injects repository secrets into a trusted self-hosted job.** An AI review job
  keeps working with no secret copied to the machine. Never copy secret values to the host.
- **A workflow triggered by `@mention` in comment text runs attacker-suppliable
  instructions.** A persistent host with a warm checkout is the wrong place for that. Leave
  those hosted even though they look like "just another AI job".

Point the moved jobs at your label:

```yaml
runs-on: [self-hosted, linux, <your-label>]
```

For job placement and cost, see [high-volume-ci-optimization](../high-volume-ci-optimization/SKILL.md).
Before you move an E2E suite here, read [e2e-ci-economics](../e2e-ci-economics/SKILL.md) — a faster
host hides a flaky test instead of fixing it, and the first question is whether the suite gates
anything. To find out which job to move at all, start at
[ci-speed-diagnosis](../ci-speed-diagnosis/SKILL.md).

## Register one runner per repository

A personal GitHub account has no account-wide runner: registration is per repository. Do
each one the same way, from a script rather than by hand.

```sh
token="$(gh api -X POST repos/OWNER/REPO/actions/runners/registration-token --jq .token)"
# on the host, as a dedicated non-login service account:
install -d -o runner -g runner /opt/actions-runner/REPO
cd /opt/actions-runner/REPO
curl -fsSLO https://github.com/actions/runner/releases/download/v<VER>/actions-runner-linux-x64-<VER>.tar.gz
tar xzf actions-runner-linux-x64-<VER>.tar.gz && rm actions-runner-linux-x64-<VER>.tar.gz
./config.sh --unattended --url https://github.com/OWNER/REPO --token "$token" \
  --name <RUNNER_NAME> --labels <your-label> --work _work --replace
sudo ./svc.sh install runner && sudo ./svc.sh start
```

Never print the registration token. It is short-lived, but a log is forever.

When you script this, remember that `su` starts a fresh shell: variables from the calling
script are **not** visible inside `su ... -c "..."`. Inline the directory and the token at
the point where you build the remote command, or the runner installs into the service
account's home with an empty token and `config.sh` fails.

**One runner service runs one job at a time.** A pull request with three fleet jobs runs
them one after another. Register a second service for that repository, under a different
runner name, when its queue gets long.

## Match the hosted image, or jobs fail only on your host

Workflows are written against the hosted images, which carry current toolchains. Anything
your host has at an older version fails there and nowhere else. Real example: a host with
Node 20 broke every `wrangler` step, because `wrangler` requires Node 22 or newer, while
hosted images already ship 24. Check the host's `node`, `python`, `go`, and container
runtime against what the workflows assume before blaming the workflow.

## Windows hosts: the runner lives in WSL2, and WSL will stop

Run the runner inside WSL2 and treat the Windows side as the thing that keeps WSL up. A
stopped WSL kills any job mid-step, and the symptoms do not look like "WSL stopped":

| Symptom | Meaning |
| --- | --- |
| Job steps `null` after `Checkout` succeeded | WSL went down under the job |
| Run sits in `queued` while the runner looks idle | no WSL, so no listener |
| Runner API reports `offline busy=true` | GitHub still holds the dead session |
| Journal shows `A session for this runner already exists` and `Runner connect error: Conflict` | restarted runner cannot reclaim the session yet; it clears in a minute |

Two things hold WSL up, and you need both:

- `%USERPROFILE%\.wslconfig` with `[wsl2]` and `vmIdleTimeout=-1`, so the VM does not stop
  when its last client exits. A `.wslconfig` change needs `wsl.exe --shutdown` to apply,
  which kills running jobs — only do it while the fleet is idle.
- A scheduled task holding a WSL process open:
  `wsl.exe -d <distro> --user <runner-user> -- bash -lc "exec sleep infinity"`. Give it an
  **at-startup trigger** and principal `LogonType=S4U`, which needs no interactive session
  and no stored password. A task with the default `LogonType=Interactive` never fires on a
  headless desktop — check with `quser`; on a machine nobody logs into, it returns nothing.

Register the task without touching an existing one:

```powershell
$a = New-ScheduledTaskAction -Execute "C:\WINDOWS\System32\wsl.exe" `
  -Argument '-d <distro> --user <runner-user> -- bash -lc "exec sleep infinity"'
$p = New-ScheduledTaskPrincipal -UserId "<HOST>\<user>" -LogonType S4U -RunLevel Limited
$s = New-ScheduledTaskSettingsSet -StartWhenAvailable -RestartCount 3 `
  -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit ([TimeSpan]::Zero)
Register-ScheduledTask -TaskName "CI WSL Keepalive" -Action $a `
  -Trigger (New-ScheduledTaskTrigger -AtStartup) -Principal $p -Settings $s
```

Verify it holds: read WSL `uptime`, wait a few minutes with no SSH session attached, read
`uptime` again. If it climbed, the fleet survives idle.

Also useful on a Windows host: native OpenSSH may use PowerShell as its default shell, so
a remote command is PowerShell, not `sh`. Nested quoting breaks constantly — send a bash
script as base64 and decode it on the far side instead of fighting the quoting.

## Keep the runner disk off the OS drive

The runner's checkouts, caches, and build output all land inside the WSL2 distro's
virtual disk (`ext4.vhdx`). By default that disk sits on the OS drive under
`%LOCALAPPDATA%\Packages\...\LocalState`, and it only grows — WSL never shrinks it, even
after you delete files inside the distro. A fleet of per-repository runners fills the OS
drive within months (one real host: 22 runners, ~160 GB of `_work` checkouts, OS drive at
88 %). Put the distro on a data drive instead of fighting the OS drive:

```
wsl --manage <distro> --move D:\wsl\<distro>
```

The move shuts the distro down and copies the whole `ext4.vhdx`, so run it while the fleet
is idle. Every runner is a systemd service *inside* the distro, so they all move with it
and reconnect on the next boot — no re-registration.

Two failure modes before you run this on a busy host:

- **`--move` can hang on finalize.** It copies to the target, updates the registry
  `BasePath`, then deletes the source — and can wedge on that last step, leaving the disk
  on both drives with the OS-drive copy still present. Kill the stray `wsl.exe` processes,
  then, once the registry already points at the data drive, delete the old
  `LocalState\ext4.vhdx` yourself to reclaim the OS drive.
- **A stuck `wsl.exe` wedges the service.** Any wsl command (even `wsl -l -v`) issued while
  a move is mid-flight can leave the service in `StopPending`, and every later wsl call
  hangs. The Store build of WSL runs as the **`WSLService`** service, not the legacy
  `LxssManager` — restart *that* to clear it. Then cold-start the distro
  (`wsl --terminate <distro>`, then invoke it) so systemd boots and auto-starts the runner
  services; a plain `wsl -d <distro> -e ...` can enter without booting systemd, and then
  `systemctl` reports `Failed to connect to bus`.

## Known job that cannot move

`gitleaks-action@v2` scans fine on a self-hosted runner and then fails uploading
`results.sarif`: it resolves the artifact root from the runner's home directory, which is
not a parent of a workspace under `/opt/actions-runner`. The error reads `The rootDirectory:
/home/<user> is not a parent directory of the file: .../results.sarif`. Leave that job
hosted and say why in the workflow, so nobody re-moves it later.

## Toolchains the hosted images have and your host does not

`prepare-host`-style setup is not finished after Node. Every one of these was found by a
job that passed on GitHub and failed only on the fleet host:

| Missing | Symptom | Fix |
| --- | --- | --- |
| passwordless sudo for the service account | `sudo: a password is required` | a `NOPASSWD` line in `/etc/sudoers.d/` |
| Docker | `docker: command not found` on any workflow using `services:` | Docker Engine, plus the service account in the `docker` group; restart the runner services so the group applies |
| Rust | `failed to run 'cargo metadata'` on Tauri builds | install to a shared prefix, then symlink the **toolchain** binaries into `/usr/local/bin` — not the `rustup` shims, which need `RUSTUP_HOME` that a per-service `HOME` does not have (`rustup could not choose a version of cargo to run`) |
| `xdg-utils`, `desktop-file-utils` | `failed to bundle project xdg-mime binary not found` | install both |

The general rule: a hosted image is a large pile of preinstalled tooling, and every piece
of it your host lacks becomes a failure that reproduces nowhere else. Fix it on the host
rather than adding install steps to the workflow, or the workflow slows down for everyone.

## A fixed-port service container cannot run twice on one host

This is the hard ceiling on a single-machine fleet. A job that declares

```yaml
    services:
      postgres:
        image: postgres:16-alpine
        ports: ["5432:5432"]
```

binds host port 5432. Hosted runners give every job its own VM, so three parallel test
shards each get their own 5432. One machine cannot: the second shard dies with
`Bind for 0.0.0.0:5432 failed: port is already allocated`.

So a repository whose parallel jobs use fixed-port service containers gets exactly **one**
runner service, and its jobs serialize. If that queue is too slow, the fix is an ephemeral
per-job runner (a cloud runner service), not more runner services on the same box.

## Remote-development tools are a separate problem

A synced remote-dev tool (Crabbox and similar) verifies the workspace it just synced by
fetching the target commit from the forge **on the host**, with Git's config neutralized
(`GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`, `GIT_CONFIG_NOSYSTEM`, and sometimes
`-c credential.helper=`). That verification is where these tools break on a self-hosted
host, and the failure message is usually generic: "remote git seed failed", "align remote
Git metadata".

**Test the auth assumption before you act on it.** The obvious theory — neutralized config
means no credentials means private repositories cannot be fetched — was wrong on a Windows
host here. Git for Windows cloned a *private* repository with
`GIT_CONFIG_GLOBAL=NUL GIT_CONFIG_SYSTEM=NUL` and no credential config, silently and
successfully. Reproduce the tool's exact command on the host before rebuilding your auth
around a guess (this cost real time, and produced two SSH keys and a deploy key that turned
out to be unnecessary):

```powershell
$env:GIT_CONFIG_GLOBAL="NUL"; $env:GIT_CONFIG_SYSTEM="NUL"; $env:GIT_TERMINAL_PROMPT="0"
git clone --quiet --filter=blob:none --no-checkout --single-branch --branch main <url> $tmp
```

One real and generalizable cause of these failures on Windows: **PowerShell with
`$ErrorActionPreference = "Stop"` turns anything a native command writes to stderr into a
terminating error.** Recent OpenSSH clients print

```
** WARNING: connection is not using a post-quantum key exchange algorithm.
```

to stderr on *every* connection, so a perfectly successful `git clone` over SSH kills the
script that called it. Silence it per host in the host's `~/.ssh/config`:

```
Host github.com
  LogLevel ERROR
```

After that, `git clone` produced zero stderr lines here. Verify with
`@(& git clone ... 2>&1).Count` rather than assuming.

Two more notes worth carrying:

- These tools verify that the commit you are syncing is **on the branch they advertise**.
  A local branch you never pushed fails with something unhelpful ("requested commit is not
  on advertised branch"), and it is not a host problem — push the branch.
- Do **not** "fix" Git Credential Manager noise on Windows (`Unable to persist credentials
  with the 'wincredman' credential store`) by switching the store to `dpapi`: the fetch then
  hangs on an interactive prompt instead of printing a harmless warning, and you have to
  kill the stuck `git` and `git-credential-manager` processes.

If the tool still fails after all of that, replicate each of its steps by hand on the host.
When every individual step passes and the tool still fails, the bug is in the tool, not in
your host — file it upstream with that evidence instead of rebuilding your machine around it.

## Before you build one: what it costs to own the machine

This skill came out of a real fleet — fifteen private repositories, one Windows desktop,
runners in WSL2 — that was **retired within days** for managed ephemeral runners
(Ubicloud). Not because the idea was wrong, but because of what a single owned machine
actually costs once it is load-bearing.

**What it delivered.** Per job, the box beat the hosted runner: no queue wait, warm caches,
zero minutes billed. On an idle host, jobs finished in roughly the same wall clock as a
managed runner and sometimes faster.

**What it cost.**

| Cost | What it looked like |
| --- | --- |
| Fixed concurrency | One runner service runs one job at a time. A busy day meant ~30-minute queues while a managed runner would have started every job at once. |
| A ceiling you cannot script past | A `services:` container on a fixed host port cannot run twice on one machine, so sharded test jobs serialize. |
| Image drift, forever | Every hosted-image tool the host lacks is a red job that reproduces nowhere else. Docker, Rust, `xdg-utils`, `gh`, `jq`, a current Node — each found the hard way. |
| Outages that look like nothing | Three separate outages in one day, all reading identically on GitHub as "runner offline". Nothing alerts by default. |
| Invisible failure once a second tier exists | When managed runners absorbed the load, CI stayed green through every outage. The fleet was down for hours and nobody noticed. |

**The decision rule.** Self-hosted wins when you need something the managed tier cannot
sell you: a GPU, a specific OS or kernel, hardware attached to the machine, a licence tied
to a host, data that may not leave your network, or genuinely enormous monthly minutes.
Speed alone is not on that list — per-job speed was a wash, and per-job isolation is worth
more than warm caches on anything with parallelism.

**If you own one anyway, own it properly.** Two tiers is the stable arrangement: managed
ephemeral runners carry the fleet, the owned host takes work that needs it. Then a health
check that **exits nonzero** when the host is unreachable or a runner is offline is not
optional — a second tier hides the first tier's outages completely, which is exactly how a
fleet stays broken for a day.

## Verify, then move on

Run a harmless command on the host first. Watch the first fleet run to completion rather
than assuming. Read review feedback before merging. Use an isolated worktree per change,
and remove it after merge.
