# Open-source repos for hooks, scripts and video ads

Found on 2026-11-10 with `gh search repos`. "Read" means I opened the files. "Listed" means I saw only the name and description. Check the date again before you rely on a repo.

Licences: GitHub's licence field was unreliable. It printed "no licence" for repos that have one. Read each repo's LICENSE file before you copy anything. Read the repos below for ideas and write your own text unless the licence allows more.

## How to search again

Put the filters in the query text. There is no `--pushed` flag.

```bash
gh search repos "video hooks pushed:>2026-08-15 stars:>=25" --sort stars --limit 8 \
  --json fullName,description,stargazersCount,pushedAt \
  --jq '.[] | "\(.stargazersCount)★ \(.pushedAt[:10]) \(.fullName) — \(.description[:100])"'
```

`--sort updated` lists tiny repos that someone touched today. Sort by stars with a `pushed:` filter.
Many hits are noise (React hook libraries match "hooks"). Use phrases such as "hook formulas", "short-form video script", "ugc ad".

## Hooks and short-form scripts

| Repo | Stars | Pushed | Status | What it offers |
|---|---|---|---|---|
| [sergebulaev/tiktok-skills](https://github.com/sergebulaev/tiktok-skills) | 123 | 2026-11-04 | Read | Ten 3-second hook formulas, each with a spoken line, on-screen text and first image. Engagement goals per formula. Our [hook-formulas](hook-formulas.md) are a rewrite of the ideas. |
| [shixinzhang/tiktok-viral-hooks](https://github.com/shixinzhang/tiktok-viral-hooks) | 43 | 2026-11-07 | Read (README) | Daily teardowns of viral TikToks, by niche and hook pattern, with a two-sentence template each. Licence CC BY-NC-SA 4.0: ideas only, no copying. |
| [Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) | 5812 | 2026-09-13 | Listed | Claims 26 scored Reel hook formulas (`skills/ig-reel/hooks.json`, `hookscore.py`). Worth a read for the scoring idea. |
| [Melvynx/video-agent-skills](https://github.com/Melvynx/video-agent-skills) | 142 | 2026-11-06 | Listed | Markdown skills to script, research and edit short videos. |
| [Yuzzyuk/marketing-os](https://github.com/Yuzzyuk/marketing-os) | 575 | 2026-08-17 | Listed | Marketing skill with an 18-tactic hook engine. |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | 59580 | 2026-11-10 | Listed | Large marketing skill set: copywriting, CRO, analytics. |

## UGC and ad video

| Repo | Stars | Pushed | Status | What it offers |
|---|---|---|---|---|
| [charlesdove977/UGC-Factory](https://github.com/charlesdove977/UGC-Factory) | 97 | 2026-10-23 | Listed | UGC video ad factory: Higgsfield and Seedance 2.0, genre style skills. |
| [zutrue/zuverse](https://github.com/zutrue/zuverse) | 14 | 2026-11-03 | Listed | Reverse-engineers a video ad and remakes it shot for shot with a new person. Use only on your own or licensed ads. |
| [Reviral-ai/awesome-ai-ugc-ad-prompts](https://github.com/Reviral-ai/awesome-ai-ugc-ad-prompts) | 1 | 2026-08-26 | Listed | Fill-in UGC ad prompts. Very small. |

## Build and render

| Repo | Stars | Pushed | Status | What it offers |
|---|---|---|---|---|
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | 82255 | 2026-11-10 | Used in `ship-demo-video` | HTML to video for agents. |
| [latent-spaces/brag](https://github.com/latent-spaces/brag) | 20962 | 2026-10-23 | Used (MIT) | Launch-video skill for HyperFrames, with five example storyboards. |
| [cathrynlavery/yap-studio](https://github.com/cathrynlavery/yap-studio) | 48 | 2026-11-10 | Used (Apache-2.0) | Talking-head editor and its card vocabulary. |
| [remotion-dev/template-tiktok](https://github.com/remotion-dev/template-tiktok) | 306 | 2026-11-09 | Listed | TikTok-style captions with Whisper.cpp in Remotion. |
| [DojoCodingLabs/remotion-superpowers](https://github.com/DojoCodingLabs/remotion-superpowers) | 165 | 2026-10-29 | Listed | Video production skills for Remotion. |
| [daviddinkevich/Story2Board](https://github.com/daviddinkevich/Story2Board) | | | In `launch-video-generation` | Locked-reference method for a consistent character. Not rechecked on 2026-11-10. |

## Not evaluated

Large storyboard platforms, mostly in Chinese: `HBAI-Ltd/Toonflow-app`, `ArcReel/ArcReel`, `waooAI/waoowaoo`. They target drama and comic video, not ads.

## When you add a repo

Add a row with the date, the status (Read or Listed) and the licence you saw in the LICENSE file. Add a dated line to the lessons log in `SKILL.md`.
