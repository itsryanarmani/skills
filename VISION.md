# Vision — pooriaarab/skills

## What this is

A collection of Claude Code skills for AI-aware development and life organization. Each top-level directory holds one skill: a Markdown playbook that teaches the agent one job. The collection holds about 190 of them. Forty-eight of the forty-nine ad-platform skills share one conversion-tracking contract, `ad-conversion-hub`, which owns events, consent, hashing, deduplication, and failure isolation; `ads-google` runs its own GA4-based scheme instead. A 25-skill organizer suite sorts files, notes, mail, calendars, contacts, photos, and code. Seven CI skills diagnose speed, cost, and queueing on repos where agents open most pull requests. Standalone skills deploy an app to five targets (self-hosted, Cloudflare, GCP, AWS, Azure), walk it through vendor marketplaces and directory listings, and run personal admin such as the Canada census and a Schengen visa application.

## Who it is for

The owner: a solo developer who ships products with coding agents as the main workforce and pays the token, CI, and runner bills personally. The skills assume that reader. `ci-cost-at-agent-scale` fixes repos "where agents open most of the pull requests". `delegate-implementation` plans with an expensive model and implements with a cheap one to cut cost. The organizer suite, the census skill, and the visa skill act on one person's files, preferences, and paperwork. The census and visa skills store no PII; the organizer suite does hold user data, because mirroring notes and contacts is what it is for. A second reader — anyone who copies a skill into their own setup — benefits but does not drive design.

## What good looks like

- An agent completes a task end to end from one skill and stops where a human must act — the census skill fills the StatCan form and halts before submit.
- A skill that a live run contradicts gets corrected in place, and the commit names that run — "Correct both integration skills from a live submission".
- A cost skill shows a before/after number on the owner's own usage: ~65% less token use (eco-mode), ~45% lower cost (agent-context-economy), 50–80% savings from delegated implementation.
- A CI optimization lands only after a measurement names the constraint: latency versus machine seconds first, then the critical path, then cache health.
- A life-admin skill handles personal data without storing any of it. `canada-census` and `schengen-visa-application` both state "Zero PII".

## Explicitly not this

- An application or an installable package. The root has no `package.json` and no source tree; every top-level entry is a skill directory, a top-level doc (README, AGENTS, this file), or a directory that holds sub-skills or shared docs rather than a `SKILL.md` of its own (`organizer/`, `brand/`, `docs/`). A runtime, a CLI binary, or an npm module does not belong here.
- A new platform ad skill with its own tracking scheme. `ads-google` is the sole existing exception, kept for its GA4 layering; every other platform skill takes events, consent, hashing, deduplication, and failure isolation from `ad-conversion-hub` and must reuse that contract, not redefine it.
- A rewrite of a live-verified step from vendor documentation. The commit log corrects skills from live submissions, real campaigns, and real portals; a live run outranks the doc the text came from.
- A second entry point for a domain the repo already routes. CI starts at `ci-speed-diagnosis` and life organization starts at `org-life-organizer`; a parallel router for the same domain splits the path every new reader must start on.
- A life-admin skill that stores personal data. The census and visa skills state "Zero PII" and stop before irreversible steps; a skill that saves that data breaks the property they state.

## How it pays for itself

Nobody sells this repo: the README names no product or price, and the commit log ships skills, not releases. It pays the owner back in money and time. The cost skills put numbers on it: 50–80% savings from delegating implementation to cheaper models, ~65% less token use from eco-mode, and a CI bill that stops growing with every agent-opened pull request. The platform skills pay in avoided re-learning: each vendor playbook is written once and corrected after a live run, not rediscovered each time.

## The current bet

As of 2026-08-31, the bet is that this collection works as the operating manual for one operator's agents — real products, real hosts, real ad campaigns — and that live use keeps correcting it faster than the platforms drift; test it by 2026-11-30 against the commit log, where "Correct" commits should keep landing beside the adds.
