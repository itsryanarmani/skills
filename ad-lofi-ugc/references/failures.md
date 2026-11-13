# Failures we hit, and the fix

Every entry cost time or money. Check this list before a batch.

## Prompts and images

| Failure | What happened | Fix |
|---|---|---|
| Garbled text on "blank" signs | Asked for a taped notice / yard sign; even "completely blank white sheet, zero letters" prompts produced readable junk letters on 2 of 3 tries | Keep text out of generated images entirely. Ask for "zero letters, zero signature", QA every still, and paint all real text in HTML/ffmpeg overlay |
| Rotated 90° image | A generated photo came back landscape-in-portrait, sideways | Add an orientation check to QA: view every still full-size, check EXIF, look at horizons and doorframes. Caught only by looking, not by any mechanical check |
| Almost-sideways shipped ad | One degrade output was nearly sideways; the tilt was baked into the generation, not the crop | Same fix — inspect the raw candidate before blaming the degrade |
| Melted hands | A seed still had a melted foreground hand and fingerless subject hands | Rejected at seed QA before spending on video; "Correct five-finger hands" in the prompt helps but does not guarantee |
| Black corners after tilt | The degrade's small rotation exposed black edges | Crop the centre 90% right after the rotate (93% still leaves a dark corner at 3 degrees). A plain scale-down then up does not hide them. Measure corner brightness to check. |

## Video

| Failure | What happened | Fix |
|---|---|---|
| Phone became a notepad | A held phone morphed into a yellow notepad mid-clip | Mandatory object-continuity QA: frames every 0.5 s, list held objects in frame 1, confirm each persists. Regenerate from the predecessor's last frame |
| Clip morphed into a new person | A drive-by clip invented a person holding a phone with garbled camera UI | Stronger negative block in the motion prompt ("Do not add a person. Do not add a phone. Do not cut. Do not zoom in."), regenerate |
| Clips 5.37 s, not 5 s | Caption timing assumed exact shot boundaries | Normalize every clip to the exact duration (`-t 5.0`) before concat |
| Silent videos | Round-two videos shipped with no audio; owner flagged it | Muted-first design plus a sound pass: VO + quiet bed + sparse ffmpeg SFX, AAC out, and a `_muted.mp4` export as proof |
| `drawtext` missing | ffmpeg on the run machine had no drawtext filter | Render captions as transparent PNGs in headless Chrome (exact letters, web fonts), overlay with ffmpeg `overlay=enable='between(t,s,e)'` |

## Process and money

| Failure | What happened | Fix |
|---|---|---|
| Two writers clobbered one spend log | Two `gen.py` processes raced one `spend.json`; 8 call records lost and reconstructed by hand | One writer per spend file. `flock` around read-modify-write, temp file + atomic rename, reservations logged before the call |
| Trusted the account balance | Another worker shared the API key, so balance deltas did not equal our spend | The spend file is the only meter. Never read the wallet to measure your batch |
| nohup/background worker killed | Long-running generation jobs died when the supervising shell or session ended | Run workers in a persistent session or service that survives, checkpoint after every billed call, and make the job resumable (skip outputs that already exist) |
| Rebuild re-ran paid calls | A re-run of the build script re-submitted every generation | Skip a shot/image when its output file already exists; never resubmit to "refresh" |
| Launch script and prompts not saved | The first campaign's launch spec and creative prompts were never committed; the funnel had to be reverse-engineered | Save every prompt, motion prompt, TTS script and the manifest JSON in the repo before the batch ends |
| Curl argument too long | Inline JSON body in `curl -d "$body"` died: argument list too long | Write the JSON to a file and use `-d @file` |

## Ad-library API traps (from the research run)

| Failure | What happened | Fix |
|---|---|---|
| Fuzzy brand-name lookups | `companyName` search returned the wrong brand | Resolve the official page/advertiser id first, then query by id |
| Empty result read as "no ads" | `not_found` / empty responses on routes that should have data | Treat as "not returned"; cross-check another route before concluding |
| Wrong request field | `/facebook.ad_details` wants body field `id`, not `adId` (400, unbilled) | Check the endpoint's input schema before the first call |
| TikTok name+region conflict | Sending `advertiserName` with `region` returns 400 | Drop one parameter |
| Expected US TikTok coverage | The TikTok Ad Library serves EU/EEA only | Do not plan around US TikTok data from it |
| Google Transparency has no RSA copy | Returns format + dates + preview, not headline text | Use a paid SERP tool for the actual copy |
| Organic SERP read as "zero ads" | Scrapers silently omit the `ads` array | An organic-only response is not evidence of no competition |
| Ad-library HTML fetches | Pages timed out / automation rejected | Use the official API or export the platform offers (for example the Meta Ad Library API). Never fake a browser User-Agent to get past a block. |
| Wrong balance endpoint | `GET /v1/balance` and `/v1/whoami` on Monid return 404 | Balance is `/v1/wallet/balance`; `whoami` does not exist |
| Tiny test budget, no signal | A few dollars over 7 days produced ~56 impressions; no creative could be judged | Size budget so each ad clears a few hundred impressions before reading results |
| Invalid insights field | Meta rejected `ctr_all`; the whole query failed | Validate field names before requesting; pull ad-level breakdowns, not campaign aggregates |
| Dead gaps in a video | Fixed 2.8 s shots were laid over a voice track that was never measured. The sound ended and the scene did not change | Build the timeline from the measured length of each voice line. Fail any stretch where picture is static and audio is silent for over 0.3 s. |
| Video too slow | Clips ran at normal speed with 3-4 s per shot | Speed clips 1.3-1.6x, cut every 0.8-2 s, finish at 10-14 s. |
| Sounds do not match the scene | Effects and bed were not tied to events in the picture | Put a whoosh on only the cuts that reveal something (one landing whoosh beats five), a boom on the biggest beat, a record-scratch on the twist. Match the bed mood to the scene. |
| Words run together in captions | Word-by-word captions were joined without a space ("Prettyhouse.") | Render each word with its trailing space. Look at caption frames before shipping. |
| Black rectangle on a prop | A held paper showed a black box in two shots | View frames every 0.25 s and cut away before the artifact, or crop it out. |
| Sitcom did not work | Wide shots made eyes tiny and bad; one set rotated and zoomed; the characters did not speak; no laughter | Use mediums and close-ups for speech, build real camera angles from the same set, drive lips with an audio-driven talking model, add a licensed laugh track. |
| Worker hung on stdin | `codex exec` and `pi` with no closed stdin did nothing for 30-40 min | Start background workers with `< /dev/null`. Long research jobs on a slow model hit a 30 min limit, so save the output file early. |
