# itsryanarmani/skills

Claude Code skills for AI-aware development and life organization.

## Web performance

Use [web-performance-evidence](web-performance-evidence/SKILL.md) to measure fonts, caching, API payloads, page loading, and server work.

## Ad tracking skills

These skills share the `ad-conversion-hub` contract. Use the platform skill for
vendor setup and API details. Use `ad-conversion-hub` for canonical events,
consent, hashing, deduplication, and failure isolation.

### Tier 1: search and social

| Skill | Platform |
|---|---|
| [ads-google](ads-google/SKILL.md) | Google Ads + GA4 |
| [ads-meta](ads-meta/SKILL.md) | Meta |
| [ads-reddit](ads-reddit/SKILL.md) | Reddit |
| [brand](brand-router/README.md) | **Suite of 22.** Run a whole brand from one visual direction — voice, landing page, avatar, OG card, LinkedIn banner, Instagram carousels, YouTube thumbnails and edit style, podcast cover, decks. Start with [`brand-router`](brand-router/SKILL.md): it surveys what you actually publish and recommends a kit of three registers rather than one style. |
| [ads-microsoft](ads-microsoft/SKILL.md) | Microsoft Advertising |
| [ads-amazon](ads-amazon/SKILL.md) | Amazon Ads |
| [ads-tiktok](ads-tiktok/SKILL.md) | TikTok |
| [ads-linkedin](ads-linkedin/SKILL.md) | LinkedIn |
| [ads-pinterest](ads-pinterest/SKILL.md) | Pinterest |
| [ads-snapchat](ads-snapchat/SKILL.md) | Snapchat |
| [ads-x](ads-x/SKILL.md) | X |
| [ads-apple-search](ads-apple-search/SKILL.md) | Apple Search Ads |

### Tier 2: DSP and native

| Skill | Platform |
|---|---|
| [ads-taboola](ads-taboola/SKILL.md) | Taboola |
| [ads-outbrain](ads-outbrain/SKILL.md) | Outbrain Amplify |
| [ads-criteo](ads-criteo/SKILL.md) | Criteo |
| [ads-trade-desk](ads-trade-desk/SKILL.md) | The Trade Desk |
| [ads-quora](ads-quora/SKILL.md) | Quora |
| [ads-spotify](ads-spotify/SKILL.md) | Spotify |
| [ads-nextdoor](ads-nextdoor/SKILL.md) | Nextdoor |
| [ads-yelp](ads-yelp/SKILL.md) | Yelp |
| [ads-stackadapt](ads-stackadapt/SKILL.md) | StackAdapt |

### Tier 3: AI and emerging

| Skill | Platform |
|---|---|
| [ads-chatgpt](ads-chatgpt/SKILL.md) | ChatGPT Ads |
| [ads-perplexity](ads-perplexity/SKILL.md) | Perplexity Ads |
| [ads-copilot](ads-copilot/SKILL.md) | Microsoft Copilot Ads |
| [ads-meta-ai](ads-meta-ai/SKILL.md) | Meta AI Ads |

### Tier 4: regional and CTV

| Skill | Platform |
|---|---|
| [ads-baidu](ads-baidu/SKILL.md) | Baidu |
| [ads-tencent](ads-tencent/SKILL.md) | Tencent |
| [ads-douyin](ads-douyin/SKILL.md) | Douyin / Ocean Engine |
| [ads-weibo](ads-weibo/SKILL.md) | Weibo |
| [ads-xiaohongshu](ads-xiaohongshu/SKILL.md) | Xiaohongshu |
| [ads-kuaishou](ads-kuaishou/SKILL.md) | Kuaishou |
| [ads-bilibili](ads-bilibili/SKILL.md) | Bilibili |
| [ads-yandex-direct](ads-yandex-direct/SKILL.md) | Yandex Direct |
| [ads-vk](ads-vk/SKILL.md) | VK |
| [ads-naver](ads-naver/SKILL.md) | Naver |
| [ads-kakao](ads-kakao/SKILL.md) | Kakao Moment |
| [ads-yahoo-japan](ads-yahoo-japan/SKILL.md) | Yahoo Japan / LY Ads |
| [ads-line](ads-line/SKILL.md) | LINE Ads |
| [ads-sharechat](ads-sharechat/SKILL.md) | ShareChat |
| [ads-moj](ads-moj/SKILL.md) | Moj |
| [ads-shopee](ads-shopee/SKILL.md) | Shopee |
| [ads-hotstar](ads-hotstar/SKILL.md) | Hotstar |
| [ads-mercadolibre](ads-mercadolibre/SKILL.md) | Mercado Libre |
| [ads-twitch](ads-twitch/SKILL.md) | Twitch |
| [ads-roku](ads-roku/SKILL.md) | Roku |
| [ads-samsung](ads-samsung/SKILL.md) | Samsung Ads |
| [ads-lg](ads-lg/SKILL.md) | LG Ads |
| [ads-strava](ads-strava/SKILL.md) | Strava |
| [ads-discord](ads-discord/SKILL.md) | Discord |
| [ads-waze](ads-waze/SKILL.md) | Waze |

## Skills

### Life organization (`organizer/`)

A coordinated suite for organizing across every digital surface — files, notes, mail, calendars, contacts, photos, social bookmarks, code. Run [`org-life-organizer`](org-life-organizer/SKILL.md) first to survey preferences and get a recommended sequence. See [`organizer/README.md`](organizer/README.md) for the full catalog (21 sub-skills) and [`organizer/DESIGN.md`](organizer/DESIGN.md) for architecture.

### CI and runners

**Start at `ci-speed-diagnosis`** — it names the constraint and routes
to the skill that holds the lever. The others assume you already know which job matters.

| Skill | Answers |
|-------|---------|
| **[ci-speed-diagnosis](ci-speed-diagnosis/SKILL.md)** — the entry point | Find out why the CI optimisations you already have do nothing, before adding more. The measure-first order (latency vs machine seconds, then the critical path, then cache health), the checklist of defects that fail silently behind a green check (a secret holding an empty value, a task runner stripping `TURBO_*` from child processes, a `.next/**` output glob that sweeps the incremental cache into a 1.2 GB artifact whose upload fails, ref-scoped duplicate caches filling the quota, `restore-keys` with no lockfile-independent fallback, Prettier's mtime cache strategy that `actions/checkout` defeats, a buffering cache server that caps uploads), the bug shape that recurs most — one host's mitigation applied on every host — and the measurement discipline that keeps the numbers honest. |
| [ci-build-speed](ci-build-speed/SKILL.md) | Make CI fast AND reliable for a Next.js + bun + Turborepo monorepo on GitHub Actions — profile to find the critical path (it's the build), cache everything, fix the build OOM (the `memoryBasedWorkersCount`-overrides-`cpus` gotcha + swap + free disk), build-once dedup, concurrency cancel, with the honest verdict on what moves wall-clock vs only CI minutes. Opens with the agent-scale question that precedes profiling: whether the build belongs on the pull request at all. |
| [e2e-ci-economics](e2e-ci-economics/SKILL.md) | Place and gate a browser end-to-end suite so it earns its cost. Why a job with `continue-on-error: true` on every push is the worst of the three states — it was the longest job in two pipelines and gated nothing — plus gating on a minimal browser set and running the full matrix nightly, why you shard instead of raising `workers` on shared mutable state (two workers sharing one dev server and one database contaminate each other; proved independent mutable state is the exception), the fixed per-shard cost that sets the floor, why an E2E result must never enter a task-runner cache, the default-branch alert that catches the suite everyone stopped reading, how to report a retry-pass, and why you address a collection member by a stable key rather than by index — an indexed assertion silently retargets the first time anything is prepended. Carries the two-step-CI placement rule — the expensive suite runs on the commit that ships, not on every pull request. Ends with what a linter can enforce here and what it cannot. |
| [high-volume-ci-optimization](high-volume-ci-optimization/SKILL.md) | Job placement and cost for CI on repos where agents open many PRs per hour. A warm Boat JIT pool for private Linux CI, collapsing job fan-out, host-local caches outside the workspace, parallelism caps, fixed-port services routing, duplicate-work filters — two-step CI: a cheap pull request, the full suite on the push that ships — collapsing default-branch CI until a real merge queue exists, affected-only builds, a shared remote cache, cache-masking hazards, and cost comparison. Cross-references `self-hosted-runner-fleet` for host setup. |
| [ci-cost-at-agent-scale](ci-cost-at-agent-scale/SKILL.md) | Fix CI cost and CI queueing on a repo where agents open most of the pull requests. Audits where the runs come from first, then fixes in cost order: take the suite off `pull_request` (the ~20-second secret scan stays; lint, typecheck and unit tests run only on high-risk paths; the build never runs on a PR), delete workflows whose steps are all ref-gated (they install and exit green), add concurrency groups, path-filter the heavy suites, share the build cache, change runners last. Carries the measured PR-vs-push numbers, the label-gated Worker preview rule, the `pull_request_target` referee job an agent cannot edit green, and the staging-deploys-wait-for-green gate. Explains why the real ceiling is concurrent-job limits rather than minutes, why a review bot's fix commits multiply every other workflow, and why agent sandboxes cannot replace a CI runner. |
| [ci-runner-indirection](ci-runner-indirection/SKILL.md) | Move many repositories to a new Actions runner provider and make the next move a one-variable change: a `runs-on` variable with a default, a codemod that skips macOS, matrix and block scalars, one small PR per repo, and the traps (hosted jobs, tests that assert the label, JSON-style keys, policy labels, API rate limits). |
| [ci-speed-and-cost](ci-speed-and-cost/SKILL.md) | Twelve CI tactics with the measured result and the trap beside each. The type-checker swap that cut a runner step from 34.5 s to 2.5 s (and the false green it hides), two caches that lost time and a third that saved about 0 s, gating an 8-shard matrix on a cheap check, step timeouts, why a red scheduled suite saves nothing until it is green, affected-only selection with a mutation-tested selector, runner pools, local push gates, and one-PR-per-repo fleet rollout. Reached from `ci-speed-diagnosis`. |
| [ci-selective-evidence](ci-selective-evidence/SKILL.md) | Qualify test reports before selective CI — the second step after taking the suite off `pull_request`, never the first, with the full run on the default branch as its fail-safe. Why exit code, test outcome, cancellation, timeout, skip, retry, and missing evidence are distinct results, why missing evidence falls back to full coverage, the reader and planner controls a report reader must pass before it gates anything, how to guard proof paths and keep refusal reasons, when isolated browser workers qualify, and how to prove a relocated build still runs with the producer absent. |
| [self-hosted-runner-fleet](self-hosted-runner-fleet/SKILL.md) | Use a warm Boat JIT runner pool for private Linux CI. Covers labels, the broker and agent split, caches, one job per Box, pool wall-time costs, and the retired desktop procedure for hosts that need special hardware. |

### iPhone agent

Drive the owner's iPhone with [iphone-agent](iphone-agent/SKILL.md) through esp32-iphone-agent, UxPlay name iPhone Agent, and an ESP32-S3 USB HID mouse on AssistiveTouch. A recipe step is written only after the phone shows it. Messages, Safari, Phone, Settings, Mail, T3 Code, Notification Centre, Facebook, Instagram, and TikTok are verified opens. TikTok leave is not verified.

`npx skills add itsryanarmani/skills/iphone-agent`

### Standalone

| Skill | Description |
|-------|-------------|
| [live-site-security-sweep](live-site-security-sweep/SKILL.md) | Scan every repo that serves a live domain with the claude-security method, then fix, review, merge and release each finding. Covers headless plugin runs, a Box fleet with non-Claude agents, Cloudflare TLS and HTTPS hardening, a header baseline, and the traps from the first run. |
| [black-october-hardening](black-october-hardening/SKILL.md) | Audit and harden a Mac during a browser and Electron patch window. Finds old Chromium in Electron apps and automation caches, then lists the fixes and the traps from the first run. |
| [eco-mode](eco-mode/SKILL.md) | Cut token/CO₂ usage ~65% without quality loss. Caveman-inspired. |
| [eco-analyze](eco-analyze/SKILL.md) | `/eco-analyze` — calculate your real carbon footprint from Claude Code history |
| [multi-account-cli](multi-account-cli/SKILL.md) | One-command switching between work and personal accounts across gcloud, gws, Firebase, and Netlify. |
| [personal-credentials](personal-credentials/SKILL.md) | The personal credential fleet — four Claude Pro/Max subs on one macOS machine: the two token classes that decide who can be auto-routed (setup-token = inference-only vs fullscope OAuth), the keychain session scheme, private-repo-4944/CodexBar token stores and their 403-driven "no healthy account" drift, the `claude-subs-resync` repair loop, and Instinct vault seeding — including the allowlist of what an agent-facing vault should never hold. |
| [cliproxy-hub](cliproxy-hub/SKILL.md) | One always-on CLIProxyAPI hub on the home Mac. Every other host runs Claude Code or Codex through it over Tailscale. Covers the two hard rules, health check, dead-seat repair and relogin, and client wiring. |
| [chrome-profile-fleet](chrome-profile-fleet/SKILL.md) | One Chrome profile per online identity — work, personal, per-subscription, per-domain — so sessions never mix. Covers the safe Local State recipe (browser fully quit, backup first, bundled automation Chromes share the process name), the `Purpose (email)` naming convention, the three mailbox shapes (hosted mailbox / routed alias / plus-alias), Gmail send-as through Google's own SMTP (app password + `include:_spf.google.com` — mandatory on `p=reject` DMARC domains), and Cloudflare Email Routing's one-rule-one-action-per-address constraint. |
| [delegate-implementation](delegate-implementation/SKILL.md) | Orchestrator-implementer pattern for 10+ PR campaigns. Opus plans, Gemini Flash / Haiku / GPT-5 mini / Cursor Composer 2.5 implements. 50-80% cost savings vs all-Opus. |
| [agent-avatar-system](agent-avatar-system/SKILL.md) | Give every agent, user, or tenant a generated avatar derived from its name — deterministic, nothing stored, nothing chosen. Take a generator's body (blobatar/DiceBear) and draw your OWN face on it, so the roster gains silhouette variety without losing brand identity — most of those libraries are pose-only and structurally cannot draw a mouth. Pin colour to a fixed brand hue set: one locked hue collapses 60 entities to ~6 distinguishable colours, ten hues give 60 with zero collisions. Reach every surface by changing the shared display component and the mascot component, not the call sites (31 surfaces from 2 files). Covers containing the risk of parsing a library's internal output shape, compositor-only animation, and the verification that actually catches things. |
| [cheap-model-triage](cheap-model-triage/SKILL.md) | Decide when to route bulk search triage to a cheap fast model and when that is unsafe. Draws the line the usual framing gets wrong: `grep` is not the cost, reading its output is — so a cheap model compresses a result set, it never searches. Carries the two failure modes measured in practice (a cited file that was never in the input, and a missed full key on the line below a flagged partial one) and the rule that follows: delegate when a miss is cheap, never when a miss ends the task. |
| [agent-context-economy](agent-context-economy/SKILL.md) | Make a vertical agent cheaper AND more accurate by treating its context as an L1/L2/L3 cache: cache the static tool-definition prefix (~45% end-to-end cost cut, lossless), compress large tool results at insertion, lint write outputs, right-size tool count — each shipped off-by-default and promoted only through a gated before/after A/B. |
| [agent-guardrail-review](agent-guardrail-review/SKILL.md) | Review code that lets an AI agent act for a person. A checklist of the boundary bugs an independent review found in almost every one of 19 agent repos: approvals that do not bind the action that runs, data exfiltration after a private read, secret headers across redirects, container escapes, guards that fail open, and parsers that disagree. |
| [design-context](design-context/SKILL.md) | Create or audit canonical `.agents/brand.md` and `.agents/design.md` files, plus verified `/design.md` and `/brand` routes for deployed products. |
| [claude-code-mods](claude-code-mods/SKILL.md) | Build, test and publish a Claude Code mod: a plugin whose JavaScript or TypeScript hooks module runs inside Claude Code to draw panes, restyle the spinner, guard tool calls and add `/commands` with no model turn. Covers mod vs settings hook vs skill vs MCP, the static-analysis rules, `claude plugin validate` and `claude plugin test`, marketplace and directory publishing, and pitfalls reproduced on v2.1.300. Ships a tested sample mod. |
| [agent-factory-throughput](agent-factory-throughput/SKILL.md) | Unblock a high-volume multi-agent build. Eleven blockers, each as Symptom, Cause, Fix and How to verify: shared API token limits, a non-author review gate, review bots, a busy orchestrator, stacked PR merges, merge debt, command-text hooks, leaked names, recurring bug classes, VMs per agent, and lost reports. |
| [claude-code-context-diet](claude-code-context-diet/SKILL.md) | Cut the hidden per-request bloat the Claude Code CLI adds to every call — tool definitions, skill catalog, feature clusters you pay for whether or not you use them. Measure with `/context`, then trim via `settings.json`: disable unused feature clusters, deny heavy tools by name, demote rarely-used skills to user-invocable-only. Reversible, measured before/after. Client-side hygiene, distinct from agent-context-economy. |
| [canada-census](canada-census/SKILL.md) | Complete the Government of Canada Census of Population online via agent-browser — asks you each question in chat, fills the StatCan form, stops for review before submit. Zero PII stored. |
| [cloud-gpu-llm](cloud-gpu-llm/SKILL.md) | Run local LLMs (llama.cpp, GGUF) on a rented spot GPU VM on Google Cloud with the `gpu-vm` script: IAP SSH, tunnel access, cost notes and the traps from a real run. |
| [schengen-visa-application](schengen-visa-application/SKILL.md) | Prep a short-stay Schengen visa from Canada — finds the destination country's actual handler (no single "EU visa company"; consulate vs VFS/BLS vs a representing state's centre), builds the doc set from your own local files, drafts the employer support-letter request, fills the EU form, stops before the in-person biometrics appointment. Zero PII stored. |
| [bc-incorporation](bc-incorporation/SKILL.md) | Incorporate a B.C. for-profit limited company on bcregistry.gov.bc.ca via agent-browser — BCSC login (phone tap, no password), account creation, Name Request vs numbered fork, the full incorporation application, real fees and wait times, and the Vuetify gotchas. Zero PII stored; human approves every pay gate. |
| [spec-issue](spec-issue/SKILL.md) | Turn a thin Linear issue into an implementation-ready spec — grounds every claim in real code, right-sizes detail, writes test cases. |
| [backlog-triage](backlog-triage/SKILL.md) | Act as PM for an open GitHub backlog: name the release blockers, give every issue one priority, fix its labels, and append a marker-bounded brief a cheap model can execute without asking (files and lines, ordered steps, decisions made, gotchas, research, skills and URLs, done means). Research fans out read-only; one calibration pass sets priorities across the whole backlog before anything is written. Catches stacked-PR merges that read as shipped but never reached the default branch. |
| [deploy-app-self-host](deploy-app-self-host/SKILL.md) | Self-host a containerized app (Postgres + S3-compatible object store + Redis) with Docker Compose, and smoke-test it. |
| [deploy-app-cloudflare](deploy-app-cloudflare/SKILL.md) | Deploy a containerized app to Cloudflare (Workers container + D1/R2/KV/Queues/Durable Objects) and smoke-test the live URL. |
| [deploy-app-gcp](deploy-app-gcp/SKILL.md) | Deploy a containerized app to GCP (Cloud Run + Cloud SQL + Memorystore + GCS) with Terraform, verify, then tear down. |
| [deploy-app-aws](deploy-app-aws/SKILL.md) | Deploy a containerized app to AWS (ECS Fargate + RDS + ElastiCache + S3 + ALB) with Terraform, verify, then tear down. |
| [deploy-app-azure](deploy-app-azure/SKILL.md) | Deploy a containerized app to Azure (Container Apps + Postgres + Cache for Redis + Blob) with Bicep, verify, then tear down. |
| [onboard-machine](onboard-machine/SKILL.md) | Add a Windows/macOS/Linux/Android device to a personal tailnet and give it a role — controller, worker, or consumer — so it can host runners, hold checkouts, and serve dev servers the other machines can browse. The per-OS capability matrix (and why a phone is a consumer, never a worker), the ACL pattern that enforces "the controller drives the workers and nothing reaches back" in policy rather than by habit, and the five that cost real time: joining before renaming, node key expiry silently dropping a headless worker, an unscoped port-22 rule following a laptop onto hostile Wi-Fi, Windows MagicDNS failing in a way that reads as healthy, and a sleeping laptop taking a runner offline. Stops where self-hosted-runner-fleet begins. |
| [release-notes](release-notes/SKILL.md) | Draft user-facing release notes from a branch diff — filters to user-facing changes, writes in your product's voice. |
| [pr-standards](pr-standards/SKILL.md) | The pull-request rule for a repo where agents write most of the PRs: one issue, one PR, one concern, under 500 lines, and proof of the work it did. The branch/title/body shapes a checker enforces, the proof-of-work table (before/after screenshots for anything visible, a command and its result for anything else), uploading media to GitHub user-attachments instead of committing it, the `Proof: n/a` escape hatch and why an agent cannot clear its own, VISION.md as the thing a scope review judges against, which enforcement layers actually gate on a private Free-plan repo, and the rollout command. |
| [app-screenshots](app-screenshots/SKILL.md) | Capture real web-app/extension UI headlessly and beautify it into store-ready framed screenshots + promo tiles — the mock-the-host-APIs capture recipe, the `data:`-URL compositor (why `file://` breaks), exact Chrome/Apple/Play/AMO sizes, and AI hero art for marketing tiles only (never fake the product UI). |
| [android-webview-kiosk](android-webview-kiosk/SKILL.md) | Build and operate a locked-down Android WebView kiosk on a dedicated touch panel — no Android Studio, no Play Store. The hot-update path that avoids APK reinstalls, the frozen device-owner keystore trap, the renderer bad-state that only a reboot clears, and wireless-debugging persistence. |
| [browser-extension](browser-extension/SKILL.md) | Build a cross-browser (Firefox + Chrome) MV3 web extension and submit it per store — one-manifest-two-browsers layout, the CSP traps that break wasm/workers (+ the same-origin-worker fix), on-device AI (Firefox `trial.ml` / Chrome Prompt API), `web-ext`, and the full AMO (incl. mandatory 2FA) + Chrome Web Store flow. |
| [bug-bash-setup](bug-bash-setup/SKILL.md) | Plan a bug bash — balanced no-overlap test-area assignments + plan/findings-log doc, from a tester roster and time budget. |
| [bug-bash-triage](bug-bash-triage/SKILL.md) | Triage raw bug-bash findings — reconcile against the test suite, build a consolidated triage doc, then (after approval) create issues. |
| [storybook-to-design-system](storybook-to-design-system/SKILL.md) | Turn co-located Storybook stories into a live in-app design-system gallery (you pick the route name) AND fan out parallel agents to reach ~100% coverage. Stories are the single source of truth; each renders in an isolated iframe so modals/loops/logs can't hijack the page. |
| [high-fidelity-ui-image-gen](high-fidelity-ui-image-gen/SKILL.md) | Render near-pixel-faithful UI mockups with an AI image model — the prompt recipe (~94-95/100 on isolated surfaces), grounding in real source, the multi-round eval loop, the honest fidelity ceiling, and when to screenshot real HTML instead. |
| [saas-brand-system](saas-brand-system/SKILL.md) | Design a brand by fanning out many *distinct, emotion-tagged* directions in parallel — each a complete, 100%-tokenized, self-contained HTML design-system prototype under one shared contract — then review in-browser, pick one, and expand the winner into a full SaaS brand kit (logo suite, favicon/OG set, tokens, components, guidelines). Carries a 14-direction style catalog (palette/font/signature/emotion) and the gotchas (Artifact CSP blocks Google Fonts, `file://` blocked → serve http, don't build depth before the pick). |
| [verify-branding](verify-branding/SKILL.md) | Audit a web project for logo/brand-color consistency and fix the drift — one shared logo component used by BOTH header and footer, one accent hex shared by the in-app mark, favicon/icon.svg, apple-icon, OG image, and manifest, with no orphaned old colors after a rebrand. Catches the drift that hides in the asset files nobody re-opens (favicon/OG/apple-icon keep the old hex because a CSS-token rename never touches them). Pairs with `saas-brand-system`; fan out one PR per repo to standardize. |
| [embed-snippet-generator](embed-snippet-generator/SKILL.md) | Build AND verify a third-party embed/snippet catalog for a website builder or CMS with a "custom code" field — the two embed surfaces (head vs sandboxed section) and their differing tag/char-limit rules, a drill-down generator UX, and the technique everyone skips: prove each snippet RENDERS by reproducing the host's real sandbox iframe headless. Includes the gotchas — placeholder-id artifacts vs real bugs, provider embed-format drift (re-check current docs), logos via build-time manifest not runtime `onError` guessing, protocol-relative `//` in a null-origin `srcdoc`, per-account host subdomains, and why a "verified" badge is an anti-pattern. |
| [launch-video-generation](launch-video-generation/SKILL.md) | Plan and generate a short launch video — storyboard framework, wavespeed.ai API facts, the hard-won fix for scene transitions (image-to-video models anchor the scene to the input image, prompt only steers motion) and on-screen text/logos (composite real assets, don't generate them), and a $0-generation-spend path (HyperFrames) for whole-video native-app-mimicry concepts (a note, a chat thread, used as a self-aware ad). |
| [launch-video-screenwriting](launch-video-screenwriting/SKILL.md) | Write the script for a 20 to 30 second launch video — a beat sheet scaled to seconds, hook patterns, one value turn per shot, on-screen copy rules, and a call to action that reads as an afterthought. Ported from jtydhr88/screenwriting-skills; includes a worked 24 second npm-package screenplay. |
| [claude-in-cloud-browser](claude-in-cloud-browser/SKILL.md) | Run browser jobs off the local machine: Claude on the Messages API drives a cloud browser (Ichabod: remote Firefox or Chromium), many sessions in parallel. Setup, the tool loop, the limits found in real runs (concurrency cap, bot walls, no localhost, no extension pages), and what not to use it for. |
| [ci-browser-on-ichabod](ci-browser-on-ichabod/SKILL.md) | Run a CI E2E job against a cloud browser (Ichabod: remote Firefox or Chromium) instead of a browser installed on the runner. The workflow YAML, secrets, the quick-tunnel pattern, installing an extension from base64, the `moz-extension:` page limit and its iframe workaround, the session cap and retries, and timings measured in real Actions runs. |
| [ship-demo-video](ship-demo-video/SKILL.md) | Turn real footage of your own product into a 20 to 30 second social cut, repeatably: window-region capture from the test harness (privacy-safe crops, cut before the browser closes), a plain captioned cut, then a designed HyperFrames cut on a generated music bed with cuts on detected bars. Approval gates at storyboard, stills and render, plus the composition traps from a real run. |
| [slides](slides/SKILL.md) | Build a talk or pitch deck as one HTML page on a 1920×1080 stage: half the slides and half the text, huge type, a new layout on every slide, anatomy figures, verified quote cards, and designed light and dark themes. A pre-flight script renders every slide in both themes and checks words, font sizes, layout repeats, contrast, sources and quotes. Exports editable PPTX (python-pptx or PptxGenJS) and Google Slides via `gog`. |
| [livestream-workshop](livestream-workshop/SKILL.md) | Plan and run a live virtual workshop or stream: one point, a timed run of show with spare time, clip-sized blocks that each open with a 10-second hook, Q&A and demo placement, what to share on screen (deck, tool, sketch), screen-share hygiene, backups, and a news method that uses verified sources and verbatim quotes only. Hands the deck to `slides`. |
| [ship-a-product](ship-a-product/SKILL.md) | Orchestrator for idea → published launch post: sequences `build-from-template` → your own build process → `repo-standards` → `launch-seo` → `launch-video-generation` → `social-launch-post`. Points at each stage skill rather than duplicating them; enter wherever the project already is. |
| [marketing-site](marketing-site/SKILL.md) | Build the whole public site, not one page — a typed content model that generates page families (per audience, per use case, per module, per competitor), a mega-menu shell, free browser tools as an organic channel, one lead endpoint behind every form, and tests that fail when the copy starts lying. Starts from a competitor design audit so the brief comes from evidence. Carries the five expensive failures: a registry that drifts from its pages, prerendered routes that 404 only in production, delegated copy that invents plausible numbers, staging getting indexed, and a title template that was never wired. |
| [landing-page](landing-page/SKILL.md) | Design or level up ONE marketing landing page — section taxonomy (the conversion anatomy), the interaction/effect vocabulary, and the review gates, in CREATE and LEVEL-UP modes. Pairs with `impeccable` for the pixels; hand off to `marketing-site` once the product needs a page per audience or per competitor. |
| [geo-aeo](geo-aeo/SKILL.md) | Make a live site quotable by AI answer engines and usable by agents — llms.txt / llms-full.txt, per-page markdown mirrors, schema.org JSON-LD, a WebMCP manifest, answer-first structure, and programmatic entity pages. Runs after `launch-seo`; assumes the pages exist, which is what `marketing-site` builds. |
| [name-a-product](name-a-product/SKILL.md) | Find a name that is available, memorable and clear — with the order inverted: check for competing COMPANIES before checking domains, because funded competitors already sit on the `try*.ai` / `get*.com` variants a domain sweep hands you as alternatives. RDAP for bulk sweeps, Cloudflare `domain-check` for price/tier, plus the empirical map of ~14 naming lanes that are already exhausted on `.com` and `.ai` (a simple one-word `.com` does not exist at register price, in any language), the connotation checklist, and the "trying too hard" register axis. |
| [launch-seo](launch-seo/SKILL.md) | Make a newly-live docs/marketing/product site discoverable and shareable — sitemap.xml, a real robots.txt (don't trust your host's silent default), canonical/Open Graph/Twitter Card meta, a favicon, and submitting the sitemap in Google Search Console. Covers the hostname-aware robots.txt trap when staging and production share one static-asset bundle. |
| [website-directory-submission](website-directory-submission/SKILL.md) | Submit a live website to free web directories for SEO backlinks, referral traffic, and GEO/AI visibility — tiered directory tables with DR/link-type/gate, the one submission packet, the order of operations, plus the remote-MCP-server path (registry `remotes[]`, awesome-remote-mcp-servers, Glama, mcp.so) for sites with a hosted `/mcp` endpoint. Runs after `launch-seo`/`geo-aeo`. |
| [paper-submission](paper-submission/SKILL.md) | Choose a venue for a benchmark, dataset, or evaluation paper and take it from the official template through camera-ready. Decision tree, checked deadlines, anonymity and AI-use rules, checklists, and a plain arXiv skeleton. |
| [journal-reviewer-applications](journal-reviewer-applications/SKILL.md) | Become a peer reviewer for journals, conference program committees, and artifact evaluation committees — profiles to set up, free training, venue picking, how to apply per venue type, a short cover email, predatory-venue checks, an application tracker, and a CSV of venues. |
| [benchmark-publishing](benchmark-publishing/SKILL.md) | List a benchmark outside the paper: Hugging Face dataset card, the official MCP registry, Zenodo citation files, eval harnesses, paper indexes, and aggregators. One packet, filled once. |
| [launch-analytics](launch-analytics/SKILL.md) | Wire measurement into a live site/app — Google Analytics 4 (client gtag + server-side Measurement Protocol) and Microsoft Clarity — env-gated so staging never pollutes the prod property. Enforces the rule that every domain project has GA4 + Clarity + Search Console. Covers the MV3-CSP/double-fire trap (never hardcode tags in an app shell) and verifying GA4 server events via the `/debug/mp/collect` endpoint. |
| [build-from-template](build-from-template/SKILL.md) | Bootstrap a web-app-shaped idea from `private-repo-7b42` (Next.js on Workers/OpenNext, D1, R2, KV, Queues, Cron, Better Auth) instead of starting from scratch. |
| [build-a-directory](build-a-directory/SKILL.md) | Turn one niche into a monetized, SEO- and GEO-ready listing directory on Cloudflare from a directory template: the four-test niche check, a read-only domain check with a no-purchase gate, licensed listing imports behind a thin-content gate, Stripe tiers, staging on `main` and production on `release`, the `search-console` launch, and a `geoaeo audit`. |
| [claude-code-cloud-environments](claude-code-cloud-environments/SKILL.md) | Create, check, share and smoke-test claude.ai/code cloud environments (network level, variables, setup script) for your repos, and repeat it on another Claude account. The dialog is the only interface, so the skill drives it with the `cc-cloud-env` script. Covers what is safe to store, why the setup script runs in the parent of the repo, and the org-share trap. |
| [pre-public-repo-audit](pre-public-repo-audit/SKILL.md) | Audit a repo before you flip it public, and know why a clean secret-scanner run is not the answer. The five sweeps that catch what `gitleaks` structurally cannot — bare high-entropy keys with no vendor rule, absolute laptop paths (which usually name a private repo too), PII in files and commit metadata, tracked build artifacts — plus the order of operations (scan, fix, rotate, then flip) and why making a leaked repo private again rotates nothing. Runs before `repo-standards`. |
| [repo-standards](repo-standards/SKILL.md) | Bring a repo up to the repo standard — the README's front door and spine, the files around it, the About panel, real images over generated ones, the browser-only social-preview upload, translations, and the fan-out for a whole fleet. Carries the branch-protection and public-history-rewrite mechanics too. |
| [google-drive-organizer](google-drive-organizer/SKILL.md) | Reorganize a messy Google Drive into a clean folder hierarchy using `gws` CLI + AI classification. Handles untitled docs, renames, sub-folders, and empty file cleanup. |
| [notion-organizer](notion-organizer/SKILL.md) | Reorganize a chaotic Notion workspace into a clean hierarchy via the Notion MCP. Creates section pages, moves misplaced pages, classifies untitled pages with AI, and archives empties. |
| [mac-organizer](mac-organizer/SKILL.md) | Free disk space and organize files on macOS. Cleans dev caches, git worktrees, and renames files using Apple Intelligence (100% local). |
| [mac-on-windows](mac-on-windows/SKILL.md) | Make a Windows host feel like macOS — Cmd-based shortcuts, emacs text navigation, Spotlight, Quick Look, Mission Control and Spaces. Starts by detecting whether Command arrives as Win or Alt, since that decides the whole keymap. Carries the ceilings: Win+L is uninterceptable without a policy change, AutoHotkey's AltTab takes exactly one L/R-qualified modifier, and a Magic Trackpad behind a KVM forwards no multi-touch at all. |
| [windows-organizer](windows-organizer/SKILL.md) | Free disk space and organize files on Windows (locally or over Tailscale SSH). Cleans dev/build caches, sorts Desktop/Downloads into the same canonical layout as `mac-organizer`, and reconciles duplicates against Google Drive with a report-only hash + mtime classification that never deletes. |
| [knowledge-organization](knowledge-organization/SKILL.md) | Unified knowledge system across local, iCloud, Google Drive, GitHub, and Notes. Compares PARA, Zettelkasten, Johnny Decimal, LYT — recommends the right method and sets up a cross-platform context graph. |
| [personal-brain](personal-brain/SKILL.md) | Set up a private Obsidian vault + brain repo with daily git backup and Apple Notes capture. |
| [pooria-photo](pooria-photo/SKILL.md) | Create or review natural, identity-faithful generated photos of Pooria Arab for websites, profiles, articles, and social posts. |
| [files-backup](files-backup/SKILL.md) | Back up text-based documents from iCloud/local to a private GitHub repo via daily cron. |
| [inbox-triage](inbox-triage/SKILL.md) | LLM-assisted inbox processing — Claude Haiku categorizes notes, suggests filenames and wiki-links, user approves before anything moves. |
| [agentic-commerce](agentic-commerce/SKILL.md) | Let an agent buy things safely: human approves every spend, hard caps live outside the prompt, payment rails are capability-routed and inert-by-default, credentials come from a selected integration (never env), secrets never leak. Covers the 2026 rails — x402, MPP, Stripe SPT/Link, Issuing, Projects, browser-checkout. |
| [agentic-crm](agentic-crm/SKILL.md) | Let an agent read and write CRM records safely — resolve before write, provenance on every field, consent-gated outreach, merges not deletes, append-only activity ledger. |
| [agentic-phone](agentic-phone/SKILL.md) | Let an agent place and receive voice calls safely — disclosed AI identity, recorded consent, human escape hatch, hard caps in code, scoped talk track, call ledger. |
| [agentic-number](agentic-number/SKILL.md) | Manage the number inventory behind voice and SMS — acquire, capability-check, warm up, and cleanly release numbers from code with an ownership ledger. |
| [agentic-text](agentic-text/SKILL.md) | Let an agent send SMS safely — express opt-in, sacred STOP/HELP, honest sender identity, quiet hours and rate limits in code, send ledger. |
| [agentic-postcard](agentic-postcard/SKILL.md) | Let an agent send physical postcards safely — verified addresses only, human-approved creative, per-batch spend caps, idempotent sends, delivery ledger. |
| [agentic-email](agentic-email/SKILL.md) | Let an agent send email safely — authenticated domain, consent per purpose, one-click unsubscribe, bounce suppression, per-domain volume caps, send ledger. |
| [agentic-leads](agentic-leads/SKILL.md) | Run an agent-driven lead pipeline safely — provenance at capture, validate before outreach, transparent scoring, one sequence at a time, source hygiene. |
| [agentic-address](agentic-address/SKILL.md) | Keep physical addresses trustworthy — parse then verify, standardized canonical form, honest undisclosed states, verify-once cache, returns close the loop. |
| [agentic-campaign](agentic-campaign/SKILL.md) | Orchestrate multi-channel outreach safely — one sequence per recipient, global stop signals, kill-switch, composing caps, verified-outcome measurement. |
| [social-launch-post](social-launch-post/SKILL.md) | Draft and cross-post a launch announcement with video across X/LinkedIn/Threads/Bluesky/Mastodon via the Typefully API — the presigned-upload header trap, per-platform post-shape differences (LinkedIn = single post only), and why X blocks automated publishing of link-containing posts (don't try to route around it). |
| [product-hunt-launch](product-hunt-launch/SKILL.md) | Prepare a Product Hunt launch or relaunch package — eligibility checks, submission copy, maker handles, review docs, real-UI assets, browser-assisted draft entry, launch-day monitoring, and recap. |
| [ads-reddit](ads-reddit/SKILL.md) | Set up Reddit Ads pixel tracking and server-side Conversions API (CAPI) purchase attribution — Developer Portal app creation, the Conversion Access Token vs OAuth token distinction, the CAPI v3 endpoint shape, and client/server event dedup. |
| [ads-google](ads-google/SKILL.md) | Wire up Google Ads + GA4 conversion tracking — the three layers (GA4 client gtag, server-side Measurement Protocol, Ads conversion import from GA4), the MP `api_secret` that silently no-ops a server purchase when unset (distinct from the `G-XXXX` measurement id), importing/enabling/marking-Primary the GA4 conversion action, Google Ads API launch nuances (`containsEuPoliticalAdvertising` now required, text-only search ads, OAuth-project enablement), and server-side verification via the GA4 Data API + GAQL + the MP `/debug/mp/collect` endpoint. |
| [ads-meta](ads-meta/SKILL.md) | Set up Meta (Facebook) Pixel + server-side Conversions API (CAPI) purchase tracking — client Pixel and server CAPI shipped together with a shared `event_id` dedup key, the CAPI access token that silently no-ops when unset, why you fire on hashed-email match (not on `fbclid`) so organic purchases still report, advanced matching for match quality, the app-capability 400s (Advanced Access for `ads_management`, promotable Page), and server-side verification via the Graph `stats`/`last_fired_time` endpoints. |
| [ad-experiments](ad-experiments/SKILL.md) | Run paid-ad experiments on a small budget so you learn *which* variable drives signups and *why* — hyper-specific one-audience×geo×creative experiments from a written hypothesis, proving the cheapest conversion (free signup) before the expensive one, and judging on server-side truth reconciled against payment-provider ground truth, not dashboard vanity. Platform-agnostic; pairs with `ads-google`/`ads-meta`/`ads-reddit`. |
| [ad-auto-optimizer](ad-auto-optimizer/SKILL.md) | Operate live paid-ad experiments as a scheduled autonomous loop — read every channel, then adjust within hard guardrails, auto-applying only safe/reversible levers and *recommending* the learning-resetting ones. The lever tree (creative kill-gate, audience widen, LP test, budget/bid tilt, feature-utilization audit), anti-thrash + cap guardrails, loud escalation on the events that matter, and the operating truths that only surface after many cycles: platform reporting is unreliable (verify before acting), delivery-solved ≠ conversion-solved, you can't optimize what you can't measure, and budget optimizers concentrate spend. Pairs with `ad-experiments`. |
| [ad-creative-generation](ad-creative-generation/SKILL.md) | Generate photoreal ad-creative *images* with an AI image model (gpt-image-1 style) — `generations` vs `edits`, feeding a brand logo + a competitor ad as STYLE references (recreate the style, never clone marks/faces), photoreal lifestyle/product-in-context/UGC prompt patterns, the hard rule that image models garble exact text/logos/UI (those are templates, not gen), a vision-model VISUAL-QA loop that catches garbled text / warped hands-faces-objects / wrong logos and auto-regenerates failures, and batch/library organization. |
| [ad-creative-templates](ad-creative-templates/SKILL.md) | Pixel-perfect, text-precise, on-brand ad creatives at scale via HTML/CSS template → headless screenshot (many data-driven versions from one template) — when to template vs AI-gen, a catalog of high-performing styles (testimonial+pills, iMessage/social-native, bold-text-on-color, product-UI-in-context, discount/offer, founder/UGC, review-card, big-stat), Playwright/Puppeteer render at feed (1080×1080) and story (1080×1920) sizes, keeping logo/colors/fonts exact, and the truthfulness rule (real testimonials/reviews/stats/features only). |
| [ad-image-prompt-library](ad-image-prompt-library/SKILL.md) | A copy-paste library of proven ad-creative recipes — Part A: cheap pixel-exact HTML-mockup formats (the high-performing "iOS Ads" family: iMessage / Apple Notes / ChatGPT / WhatsApp chat-reveals + iPhone lock-screen notification), each with why-it-performs, the UI to reproduce, and a fill-in template; Part B: AI-image-gen prompt skeletons (photo-of-a-screen hyper-realism, Instagram pop-out, stepping-out-of-the-phone, cinematic character board, isometric figurine, OOTD collage, anime/GTA poster grid) plus the SLCT realism levers, text-in-quotes rule, and negative-prompt hygiene. Generic + reusable; pairs with `ad-creative-generation` and `ad-creative-templates`. |
| [local-business-profiles](local-business-profiles/SKILL.md) | Create a Google Business Profile for a service-area business with no public address, and a Facebook Page for the same site: the screen order, the traps (a prompt that links to an unrelated business, suggestion lists over the next field, a restored draft, a rejected description, a verification address step, a rate-limited Facebook form), the eligibility check before a fleet run, and the `gbp-create` script. |
| [localize-with-ai](localize-with-ai/SKILL.md) | Fully localize a codebase with next-intl + an LLM translation pipeline — locale-prefixed routing, per-namespace catalogs, a two-pass draft/QA-flag MT pipeline with real ICU validation, staged RTL/CJK layout work, and the non-obvious gotchas (French-source-content-hiding-as-English, per-file not per-locale freshness, auth error-code preservation). |
| [agentic-cli-npm-package](agentic-cli-npm-package/SKILL.md) | Scaffold and ship a companion tool for agentic coding CLIs as one package with three faces — a CLI, an npm library, and an MCP server — sharing a model-preference cascade core, auto-publishing to npm on a release branch. |
| [agent-harness-docs](agent-harness-docs/SKILL.md) | Author one set of agent-facing docs that work across every coding-agent harness — AGENTS.md as the single source of truth, thin per-harness pointers (CLAUDE.md, .cursor/rules, opencode.json, Codex/Gemini config), and a per-client MCP-setup section. Pairs with agentic-cli-npm-package. |
| [mcp-directory-submission](mcp-directory-submission/SKILL.md) | List a local/stdio MCP server on public directories — official registry (`server.json` + `mcp-publisher`), Smithery, Glama, PulseMCP, mcpservers.org, cursor.directory, mcp.so, Cline marketplace, mcp-get — which ones need a hosted endpoint (skip those for local-only servers) vs. accept plain npx-launched stdio, and the gotchas that cause silent rejections (100-char description cap, missing `mcpName` ownership field, npx multi-bin resolution, short-lived publish JWT). |
| [monday-app-submission](monday-app-submission/SKILL.md) | Drive a monday.com app from created to marketplace-submitted in the Developer Center UI — the long-form app management URL (a bare `/apps/manage/<appId>` 404s and looks like a wrong app id but is not), Live versions locking all branding behind New version → Draft → Promote to live, the icon crop dialog that opens zoomed in and silently crops square logos, the ~25-field workform in an iframe where Demo Link and How-to-use Link are required (record the demo before starting), verifying the install link via the 302 `oauth_payload_token` JWT, and why renaming the account URL logs out every user and must come last. |
| [cloudflare-domain-launch](cloudflare-domain-launch/SKILL.md) | Buy a domain and host a static site end-to-end from the CLI/API — Cloudflare Registrar registration, wrangler Pages deploy, custom-domain attachment, and the DNS/cert gotchas (Pages not auto-creating records, .dev HSTS preload, stale certs). |
| [registrar-transfer-to-cloudflare](registrar-transfer-to-cloudflare/SKILL.md) | Transfer a domain from Namecheap to Cloudflare Registrar from the CLI — preconditions, privacy off, the LockAction unlock, the EPP code with no API, transfer-in, mail approval, and the status poll. |
| [regional-pricing-stripe](regional-pricing-stripe/SKILL.md) | Set up regional / PPP-adjusted pricing on Stripe — `currency_options` over coupons for a pre-checkout localized-price display, discount tiers per currency (not per country), percentages sourced from real PPP data. |
| [slack-mcp-browser-auth](slack-mcp-browser-auth/SKILL.md) | Install a no-app Slack MCP server using browser session tokens (xoxc + xoxd cookie), including the Enterprise Grid `invalid_auth` fix — no Slack app or admin approval needed. |
| [crabbox-worktree](crabbox-worktree/SKILL.md) | Offload per-worktree dev work (installs, builds, dev server) to a remote GCP VM via crabbox so your laptop stays cool — bakes a golden image and wires into worktree hooks. |
| [schengen-visa-application](schengen-visa-application/SKILL.md) | Prep a short-stay Schengen (type C) visa application from Canada — finds the right per-country handler, builds the document set from your own local folders, fills the EU form, stops before in-person submission. Zero PII stored. |
| [flipper-zero](flipper-zero/SKILL.md) | Use Flipper Zero lawfully — microSD sizing, official app install via qFlipper and Flipper Lab, defensive tools, and own-device NFC, IR, and Sub-GHz checks. |

### Workspace utilities

| Skill | Description |
|-------|-------------|
| [changelog](changelog/SKILL.md) | Auto-generate a changelog from git commits since the last tag or ref. |
| [init-project](init-project/SKILL.md) | Auto-generate a CLAUDE.md for a new project by analyzing its structure, tooling, and conventions. |
| [iphone-ble-bridge](iphone-ble-bridge/SKILL.md) | Control real iPhones with no cable or Developer Mode: an ESP32-S3 acts as a Bluetooth mouse and keyboard, AssistiveTouch turns it into touches. Pairing, command protocol, button mapping, pointer scale, and the NimBLE limits that drop a third phone. |
| [stale-branches](stale-branches/SKILL.md) | List and clean up stale git branches (merged or inactive 30+ days). |
| [worktree-hygiene](worktree-hygiene/SKILL.md) | Prune git worktrees whose branches already merged, salvaging any with real uncommitted changes to a branch first. |
| [branch-deploy-convention](branch-deploy-convention/SKILL.md) | Standardise branch names onto `main` (staging) and `release` (production) without breaking a deploy. The silent-dead-trigger defect class, an org-wide sweep, the safe rename order, and the four blockers to check first. |
| [cloudflare-agent-credentials](cloudflare-agent-credentials/SKILL.md) | Get and manage Cloudflare API tokens for an agent fleet without asking a human each time. What cannot mint one (wrangler, OAuth, the MCP), the one permission that can, and minting narrow per-purpose tokens. |
| [cloudflare-cost-audit](cloudflare-cost-audit/SKILL.md) | Attribute Cloudflare spending and measure D1 row costs before changing queries, schema, or preview retention. |
| [cloudflare-worker-cost-cut](cloudflare-worker-cost-cut/SKILL.md) | Cut the Cloudflare bill of a fleet of Next.js sites on Workers (OpenNext, D1, KV). Measure each meter, find that cold starts and a few concentrated clients drive the bill, cut them in order of measured value, prove the saving in billing data, and roll it out across repos. Covers the billing feed's daily-row semantics, heavy-tail and cold-start tests, the Zone WAF token permission, and the traps from running many agents at once. |
| [cloudflare-worker-previews](cloudflare-worker-previews/SKILL.md) | Configure private-beta Worker Previews for pull requests, with branch-based URLs, safe staging bindings, live verification, sticky comments, cleanup, and dedicated test users. |
| [claude-handoff](claude-handoff/SKILL.md) | Hand off work to a background `claude` session and resume it cleanly. |
| [handoff-dictionary](handoff-dictionary/SKILL.md) | The definition of a handoff and the bar a good one has to clear — what the receiving session can actually do with what you carried. The Handoff entry from Matt Pocock's Dictionary of AI Coding, kept verbatim, plus a section on applying it: carry the why, record dead ends, reference rather than duplicate, name what is in flight, redact. |
| [git-guardrails-claude-code](git-guardrails-claude-code/SKILL.md) | Set up Claude Code hooks that block dangerous git commands (push, reset --hard, clean). |
| [x-article-publisher](x-article-publisher/SKILL.md) | Publish X (Twitter) Articles from Markdown via browser automation. |
| [spec-issue](spec-issue/SKILL.md) | Turn a thin issue-tracker ticket into an implementation-ready spec — grounds every claim in real code, right-sizes detail, writes test cases. |
| [deploy-app-self-host](deploy-app-self-host/SKILL.md) | Self-host a containerized app (Postgres + S3-compatible object store + Redis) with Docker Compose, and smoke-test it. |
| [deploy-app-cloudflare](deploy-app-cloudflare/SKILL.md) | Deploy a containerized app to Cloudflare (Workers container + D1/R2/KV/Queues/Durable Objects) and smoke-test the live URL. |
| [deploy-app-gcp](deploy-app-gcp/SKILL.md) | Deploy a containerized app to GCP (Cloud Run + Cloud SQL + Memorystore + GCS) with Terraform, verify, then tear down. |
| [deploy-app-aws](deploy-app-aws/SKILL.md) | Deploy a containerized app to AWS (ECS Fargate + RDS + ElastiCache + S3 + ALB) with Terraform, verify, then tear down. |
| [deploy-app-azure](deploy-app-azure/SKILL.md) | Deploy a containerized app to Azure (Container Apps + Postgres + Cache for Redis + Blob) with Bicep, verify, then tear down. |
| [consistent-character-images](consistent-character-images/SKILL.md) | Generate AI images of a real person that still look like them — a measured identity lock, a generate-verify-retry loop, and a vision model that scores every render against the real photographs. |
| [ui-variant-lab](ui-variant-lab/SKILL.md) | Explore a landing-page redesign by building several whole visual worlds against one frozen copy contract, comparing them in a local gallery, then promoting the winner. |
| [ui-craft-review](ui-craft-review/SKILL.md) | Review a landing page or UI artifact against a craft floor — verbatim copy, banned words, tokenized styles, the a11y floor, motion rules, interaction states, and the 390px clip check. |
| [ui-micro-interactions](ui-micro-interactions/SKILL.md) | Source and apply micro-interactions from real libraries (microkit.co, aicss.dev taxonomy, component.gallery) without over-animating. |

## Install

Via the [skills CLI](https://skills.sh). Skills live in this monorepo, so paths are `itsryanarmani/skills/<skill>`.

```bash
# Everything in this repo
npx skills add itsryanarmani/skills

# Life organizer suite entry point
npx skills add itsryanarmani/skills/org-life-organizer

# Sub-skills still nested under organizer/ (see organizer/README.md for the full catalog —
# eleven others have moved to top-level org-* skills and install individually)
npx skills add itsryanarmani/skills/organizer

# An individual organizer sub-skill (see organizer/README.md for the full list)
npx skills add itsryanarmani/skills/org-apple-notes

# An individual standalone skill — swap in any name from the table above
npx skills add itsryanarmani/skills/eco-mode
npx skills add itsryanarmani/skills/canada-census
npx skills add itsryanarmani/skills/schengen-visa-application
npx skills add itsryanarmani/skills/product-hunt-launch
```

## Data source
CO₂ rates from Jegham et al. arXiv:2505.09598 (2025). Claude Sonnet 4.6 = 0.85g CO₂/1K tokens.
