---
name: onboard-machine
description: "Add a Windows, macOS, Linux or Android device to a personal tailnet and give it a role — controller, worker, or consumer — so it can host Actions runners, hold repo checkouts, serve dev servers the other machines can browse, and accept keyboard and mouse from one controller. Use when asked to add a machine to the network, set up a second laptop or desktop as a build box, make devices reachable from each other, decide what a phone can actually do on the tailnet, or enforce that one machine drives the others and nothing reaches back. Covers the role matrix per OS, the ACL pattern that enforces control direction in policy rather than by habit, and the five failures that cost real time: joining before renaming, node key expiry silently dropping a headless worker, an unscoped port-22 rule following a laptop onto hostile Wi-Fi, Windows MagicDNS failing in a way that reads as healthy, and a sleeping laptop taking a runner offline. Stops where self-hosted-runner-fleet begins."
---

# onboard-machine

Scripts: `itsryanarmani/scripts` → `scripts/machine-onboarding/` (`onboard.sh`,
`onboard.ps1`, both idempotent).

This is the layer *under* `self-hosted-runner-fleet` and `agent-devbox`. Those
assume a machine you can already reach on port 22. This is how it becomes
reachable, and how you stop it reaching where it should not.

## Assign exactly one role

A tailnet of personal machines is not a mesh of equals.

- **Controller** — the machine you sit at. Runs the Deskflow/KVM *server*, holds
  the SSH private keys, dispatches work. Nothing logs into it.
- **Worker** — always-on or often-on. Accepts SSH, runs Actions runners, holds
  checkouts, serves dev servers. It receives; it never initiates toward the
  controller.
- **Consumer** — a phone or tablet. Joins to *reach* services. Hosts nothing.

Get the role wrong and every later decision is wrong. The most common error is
treating a laptop as a worker when it sleeps, and a phone as a worker at all.

## What each OS can actually do

| | tailnet member | inbound SSH | Actions runner | checkouts | dev server host | KVM client | KVM server |
|---|---|---|---|---|---|---|---|
| **Linux** | yes | `sshd` | yes, native — best worker | yes | yes | yes, X11 | yes |
| **macOS** | yes | Remote Login | yes, native | yes | yes | yes | yes — usual controller |
| **Windows** | yes | OpenSSH Server capability | yes, **inside WSL2** | yes | yes | yes | possible, rarely wanted |
| **Android** | yes | no | no | no | no | no | no |

**Android is a consumer and setup cannot change that.** The Tailscale app joins
the tailnet and browses `http://100.x.y.z:3000` on a worker, which is the real
reason to put a phone on it. It cannot host a runner, hold a checkout, or be a
KVM client. Two limits to plan around: Android permits exactly **one** active VPN,
so Tailscale and a corporate VPN are mutually exclusive on that device; and an SSH
server via Termux dies whenever the OS reclaims the app. Treat the phone as a
screen.

**A Windows worker runs the runner inside WSL2, never natively.** Workflows
written for `ubuntu-latest` use bash and POSIX paths and fail on a Windows runner.
WSL2 then brings a failure mode that never names itself — see
`self-hosted-runner-fleet` for the `vmIdleTimeout=-1` plus S4U-keepalive pair.

**A Linux desktop as KVM client** needs the user in the `input` group and a
`uinput` rule, and Wayland restricts synthetic input where X11 does not. If it
must accept keyboard and mouse from the controller, log it into an X11 session.

## Enforce control direction in ACLs, not in habit

If the rule is "the controller drives the workers and no worker reaches back",
write it into the tailnet policy. Convention decays; an ACL does not.

```jsonc
{
  "tagOwners": { "tag:ctrl": ["autogroup:admin"], "tag:worker": ["autogroup:admin"] },
  "acls": [
    { "action": "accept", "src": ["tag:ctrl"],   "dst": ["tag:worker:22,3000,5173"] },
    { "action": "accept", "src": ["tag:worker"], "dst": ["tag:worker:22"] }
    // No rule has dst tag:ctrl. That is the point.
  ]
}
```

With no rule whose `dst` is `tag:ctrl`, a compromised worker cannot open a socket
to the controller at all. That is stronger than "we did not install a key there",
and it survives someone later installing one.

**The KVM inverts the intuition.** Deskflow's *server* listens on 24800 and the
client connects *to it* — so the controller listens and the workers dial in. The
KVM therefore needs worker → `tag:ctrl:24800`, the one sanctioned inbound path.
Open exactly that port, and do not widen the rule because "the KVM needs the
network".

Tag at join time (`tailscale up --advertise-tags tag:worker`); tagging afterwards
means a window where the node is untagged and matches nothing.

## The five that cost real time

1. **Rename before joining.** Tailscale takes the node name from the OS hostname
   at join. Join as `DESKTOP-8F2K1A` and that string is in the ACLs, the SSH
   config and the runner labels forever. Renaming afterwards leaves a stale node
   still holding the name you want; delete it in the admin console before the good
   name frees up.

2. **Disable key expiry on every worker, at onboarding.** Node keys expire after
   180 days. A headless worker prompts nobody — it drops off the tailnet, and what
   you observe is a runner gone offline and CI queuing forever, six months after
   you last thought about Tailscale. The causal distance is what makes this
   expensive.

3. **Scope the SSH rule to `100.64.0.0/10`.** A laptop on a tailnet also joins
   airport Wi-Fi. Windows makes this worse than Linux: the stock
   `OpenSSH-Server-In-TCP` rule allows **any** remote address, so enabling the
   capability quietly publishes SSH on every hostile network the machine sees.
   Disable that rule and add a tailnet-scoped one — do not add alongside it, since
   Windows Firewall takes the union of allow rules.

4. **Windows MagicDNS fails in a way that reads as healthy.** `tailscale status`
   reports `Tailscale failed to set the DNS configuration of your device: Access
   is denied` in the health section while everything else keeps working. The only
   symptom is that `worker-hostname:3000` does not resolve and `100.x.y.z:3000`
   does. Check the health block on every Windows onboard and decide explicitly:
   fix the service privileges, or standardise on IPs for that machine.

5. **A laptop worker sleeps.** Lid closed means off the tailnet, runner offline,
   jobs queued. Either keep it awake on AC, or — better — give it its own runner
   label and pin nothing to it that a pull request waits on. Capability, not
   obligation.

## Two more that surface later

- **Dev servers must bind `0.0.0.0`.** `next dev`, `vite` and friends listen on
  127.0.0.1 by default, so the port is open in the firewall, the tailnet route is
  fine, and the connection still refuses. Use `next dev -H 0.0.0.0` / `vite
  --host`.
- **Checkouts do not travel.** Git worktrees cannot span machines and a synced
  folder (OneDrive, Dropbox, SMB) corrupts a partial clone (`blob:none`). Each
  worker keeps its own clone under a machine-scoped path; they meet on the forge,
  and the unit of exchange is a pushed branch.

## Where this stops

Once the machine answers on 22 and carries the right tag, hand off:
`self-hosted-runner-fleet` for runners, `agent-devbox` for the agent toolchain,
`crabbox-worktree` for offloading per-worktree builds.
