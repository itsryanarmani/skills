# AI video open-source landscape, 2026-11-05

Stars were read from the public GitHub API on 2026-11-05. The anime recipe in section 2 is a synthesis. A later render tested part of it: see `ship-demo-video/styles/anime-heavy-cut.md`. Rule 9 (cuts within 1 frame of a beat) held in that render; the burst lengths of 1 to 2 beats worked better than the 3 to 8 frame bursts here, which suit a 24 fps hand-drawn look and not a still-based cut.

Method: WebSearch (standard), WebFetch on READMEs, and star counts from the public GitHub API (curl, read-only) on 2026-11-05. Stars are as seen that day. Section 2 mixes sourced facts with a synthesis. The synthesis is marked "untested".

## 1. Top 12 resources

| # | Name | URL | What it does | Stars | What to steal |
|---|---|---|---|---|---|
| 1 | heygen-com/hyperframes | https://github.com/heygen-com/hyperframes | HTML + GSAP rendered to video via headless Chrome and ffmpeg. Agent skills. Apache-2.0. | 79,392 | Already our editor. Deterministic HTML timelines. |
| 2 | calesthio/OpenMontage | https://github.com/calesthio/OpenMontage | Agentic video production. 12 pipelines, Remotion and HyperFrames, 700+ skill files. AGPL-3.0. | 77,001 | Pipeline stages and production-knowledge files. Watch the AGPL. |
| 3 | remotion-dev/remotion | https://github.com/remotion-dev/remotion | React video framework. Not OSI license (company license over 3 people). | 70,987 | Frame-based composition model, caption components. |
| 4 | browser-use/video-use | https://github.com/browser-use/video-use | Edit video with coding agents. Cuts filler and dead space, 30 ms audio fades at cuts, burns subtitles. MIT. | 30,589 | 30 ms fade at every cut. Transcript-driven cutting. |
| 5 | HBAI-Ltd/Toonflow-app | https://github.com/HBAI-Ltd/Toonflow-app | Script to smart storyboard to character/scene assets to image to video. Anime short drama focus. | 20,754 | Asset-first flow: character and scene sheets before any shot. |
| 6 | Wan-Video/Wan2.2 | https://github.com/Wan-Video/Wan2.2 | Open video model. Apache-2.0. Real negative-prompt field, first/last-frame mode. | 18,386 | Local fallback model. First/last frame control. |
| 7 | Vincentwei1021/video-shotcraft | https://github.com/Vincentwei1021/video-shotcraft | Claude/Codex skill. Remotion promos, shot-card library (19 transitions, 8 rhythm shots), beat sync, sound design, frame QA. | 17,229 | Shot cards as named recipes. Separate beat-sync and sound-design rule files. (Rules not visible on README; not read.) |
| 8 | Zulko/moviepy | https://github.com/Zulko/moviepy | Python ffmpeg editing. MIT. | 15,115 | Quick scripted cuts. Not agent-native. |
| 9 | ZeroLu/awesome-seedance | https://github.com/ZeroLu/awesome-seedance | Seedance 2.0 prompt collection. | 2,818 | Anime and action prompt examples. (README not read; blurb only.) |
| 10 | YouMind-OpenLab/awesome-seedance-2-prompts | https://github.com/YouMind-OpenLab/awesome-seedance-2-prompts | 2000+ Seedance 2.0 prompts incl. anime. | 2,200 | Same. Fetch returned no README body. |
| 11 | jnMetaCode/ai-shortfilm-prompts | https://github.com/jnMetaCode/ai-shortfilm-prompts | Claude skill. 5-stage prompt structure, per-model negative-prompt table, 21 genre templates incl. transformation, mech, slow-mo. MIT. | 516 | The 5-stage order and the per-model negative table (below). |
| 12 | notivn/AIEV | https://github.com/notivn/AIEV | Claude directs HyperFrames and Remotion. Auto-cut mode, karaoke subtitles, SFX on zoom beats. MIT. | 156 | HyperFrames + SFX-on-beat wiring. Closest to our stack. |

Also seen, lower rank:
- ArcReel/ArcReel (6,156): script to assets to storyboard to video to Jianying draft. https://github.com/ArcReel/ArcReel
- zenstory-ai/drama-skills (3,822): script, assets, storyboard, prompts, review as skills. https://github.com/zenstory-ai/drama-skills
- ai-boost/awesome-image-video-prompts (3,445). https://github.com/ai-boost/awesome-image-video-prompts
- songguoxs/awesome-video-prompts (595, last push 2025-10, stale). https://github.com/songguoxs/awesome-video-prompts
- poseljacob/agentic-video-editor (507, MoviePy/ffmpeg, Gemini). https://github.com/poseljacob/agentic-video-editor
- guigulaoshi/music-video-director-skill (68, beat sync). https://github.com/guigulaoshi/music-video-director-skill
- mfahsold/montage-ai (64, beat-synced cuts, OTIO). https://github.com/mfahsold/montage-ai
- Sri01729/template-ai-storyboard-consistent-character (38, Mastra, vision consistency check). https://github.com/Sri01729/template-ai-storyboard-consistent-character
- uniqaiapp/video-director and awesome-ai-video-prompts: 0 stars, new (pushed 2026-10-28). One camera move per beat, per-model syntax. https://github.com/uniqaiapp/video-director
- Shotstack-style JSON: no popular OSS repo found. Only an unrelated profile repo (api-evangelist/shotstack, 0 stars).
- ffmpeg recipes: no popular repo found. moshspro-dev/video-effect-reel (1 star, 123 effect recipes) is tiny.

Sourced facts used below (from ai-shortfilm-prompts README):
- Prompt order: 1 style tags (3-6), 2 character and scene, 3 atmosphere and quality, 4 camera rules, 5 per-second or per-shot storyboard.
- Negatives: Veo 3/3.1 has a field; use plain nouns, not "no/don't". Kling has a field; use for artifacts (sliding feet, extra fingers, morphing). Wan has a robust field. Seedance 2.0, Runway Gen-4, Sora 2 have no reliable field: describe what you want instead.
- Consistency: identical character text in every prompt; fixed camera/lens line; reuse a negative prefab; use first/last-frame modes; Veo extend degrades after 4-5 hops.

## 2. Anime heavy-cut action recipe (untested synthesis)

Source support is thin here. The shot lengths and the shot-type list come from general anime editing practice, not from a repo that was read. Test before trusting.

**Rhythm (24 fps base; at 30 fps scale by 1.25)**
- Setup hold: 48-72 f (2-3 s). One only.
- Build: 12-24 f per shot, 4-6 shots.
- Burst (sakuga): 3-8 f per shot, 5-8 shots. Alternate wide and extreme close.
- Impact frame: 2 f, white or black, inverted colors, one hard line drawing.
- Hit-stop: hold 6-8 f right after the impact.
- Held-pose pan: 36-48 f. Slow pan over a frozen pose. It is the breath before the next burst.
- Rule: never hold a burst shot over 8 f. Never cut two shots of equal length twice in a row.

**Shot types**
- Impact frame, speed lines (radial or parallel), smear frame (1-2 f stretched motion), held-pose pan, dutch angle (10-20 deg), low-angle hero, extreme eye close-up, over-shoulder whip, sakuga burst (fast fluid limb motion on 1s or 2s).

**Keyframe image prompt template (untested)**
```
[STYLE] 2D anime, cel-shaded, flat color, hard ink outlines, limited palette of 4 colors, film grain off
[CHARACTER] <identical locked description, copied word for word every time>
[SHOT] <shot type>, <lens/angle>, <dutch tilt if any>
[ACTION] <one frozen instant of the move, peak pose>
[FX] speed lines, motion smear, impact flash, dust burst
[BG] <simple painted background, one light direction>
[LIGHT] hard rim light from <side>, two-tone shadow
```

**Image-to-video template (Veo 3.1, Kling, Seedance, Wan; untested)**
```
Start from the supplied frame. Keep the character, outfit and art style unchanged.
One camera move: <whip pan | push-in | tilt-up | locked>.
Motion: <one action in one verb phrase>, fast, snappy timing, smear frames on fast limbs.
2D hand-drawn animation on twos, flat shading, no 3D look.
Duration <3-5 s>. Ends on a held pose.
```
Keep one subject action and one camera move per clip. Cut clips down to burst lengths in the edit.

**Negative prompt list (use where the model has a field; plain nouns)**
3D render, CGI, photorealistic, realistic skin, morphing, warping, face deformation, extra limbs, extra fingers, sliding feet, flicker, color shift, blur, text, watermark, logo, subtitles, camera shake, lens flare, depth of field blur.
For Seedance, Runway, Sora: no field. Write the positive form instead ("flat cel shading, stable face, consistent outfit").

**Beat-cut pattern (untested)**
- Detect beats and downbeats first. Cut on the beat; put each impact frame on a downbeat.
- Setup on bars 1-2, build on bar 3, burst on bar 4 (cut on every 1/8 or 1/16 note), impact on the next downbeat, hit-stop for half a beat, held-pose pan across one bar.
- Add a 30 ms audio fade at each cut (taken from video-use).
- Drop the music 1 beat before the impact, then slam back in on it.

**SFX and music cues**
- Whoosh 4-6 f before each whip cut. Hit/boom on each impact frame. Short glass or metal ring after hit-stop.
- Riser through the build. Silence or low-pass on the held-pose pan.
- Music: driving drums at 140-170 BPM, taiko or breakbeat, with an orchestral hit on the downbeat. Generate instrumental only.

## 3. Ten rules for the launch-video skill

1. Lock one character description string and paste it unchanged into every keyframe and video prompt. Test: grep that all prompts contain it.
2. Build the character sheet and style anchor image before any shot. Fail the run if either is missing.
3. Put prompts in this order: style tags, character and scene, atmosphere, camera, per-shot storyboard.
4. Allow one camera move and one subject action per clip. Test: lint shot prompts for more than one.
5. Store a per-model negative-prompt table. Use plain nouns for Veo and Kling. Never write "no" or "don't" in a prompt.
6. For models with no negative field (Seedance, Runway, Sora), rewrite negatives as positives. Test: no negative block is sent.
7. Use first/last-frame mode where the model has it to pin the end pose.
8. Cap Veo extends at 3 hops. Cut instead of extending.
9. Detect beats before the cut. Test: every cut time is within 1 frame of a beat, and every impact frame is on a downbeat.
10. Add a 30 ms audio fade at every cut and run a contact-sheet check after render: one frame per shot, a flat-color or hold frame fails.

## 4. Gaps

- The shot-length and aesthetic rules in video-shotcraft were not read (they sit in files the README did not show). The pacing numbers in section 2 are a synthesis, not from a repo.
- The two Seedance prompt repos returned no README body to WebFetch. Their anime prompts were not seen, only the blurbs.
- Star counts: seen via the GitHub API on 2026-11-05 for all repos listed. Where a repo showed 0, it is new, not bad.
- No popular repo found for Shotstack-style JSON timelines or ffmpeg recipe collections. Search was limited.
- Not verified the current model lineup (Veo 3.1, Kling 3.0, Seedance 2.x/2.5, Wan 2.2) against vendor docs. Model names come from repo READMEs and search snippets.
- No public write-ups (blogs) were read in depth. Search results from pose.ai and pixeldojo were seen as snippets only.
- Remotion license and OpenMontage AGPL need a check before any reuse.
- The anime recipe was partly tested in one render (see the note at the top). The rest was not rendered or tested.
