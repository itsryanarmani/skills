---
name: video-research
description: Research a question by watching YouTube footage with Gemini. Use when the user shares a YouTube URL and asks what is in it, asks to study how a product, game, or competitor behaves on video, wants many videos analysed and the findings pooled, or asks for a mechanic, feature, or UI breakdown from footage. Triggers on "analyse this video", "watch this", "research these videos", "what do they do in this video", "study how X works".
---

# Video research

Gemini reads a YouTube URL directly. There is no download, no transcript step,
and no frame extraction. Point it at the URL and ask.

For one video, call the API. For many, use the `gameref` pipeline in
`itsryanarmani/scripts`, which caches per video and pools the findings.

## One video

```bash
TOKEN=$(python3 -c "
import json,os,urllib.request,urllib.parse
d=json.load(open(os.path.expanduser('~/.config/gcloud/adc_personal.json')))
b=urllib.parse.urlencode({'client_id':d['client_id'],'client_secret':d['client_secret'],
  'refresh_token':d['refresh_token'],'grant_type':'refresh_token'}).encode()
print(json.load(urllib.request.urlopen('https://oauth2.googleapis.com/token',b))['access_token'])")

curl -s -X POST "https://aiplatform.googleapis.com/v1/projects/YOUR_PROJECT_ID/locations/global/publishers/google/models/gemini-3.8-flash:generateContent" \
  -H "Authorization: Bearer $TOKEN" -H 'content-type: application/json' -d '{
  "contents": [{"role": "user", "parts": [
    {"fileData": {"fileUri": "https://www.youtube.com/watch?v=VIDEO_ID", "mimeType": "video/*"}},
    {"text": "YOUR QUESTION"}
  ]}]}'
```

## Many videos

```bash
gameref search "QUERY" "ANOTHER QUERY" --per-query 12 --min-seconds 180 --max-seconds 1800
gameref analyse videos.json --limit 34 --clip-seconds 600
gameref merge reports --out findings.json
```

The merge stage counts how many videos saw each finding. That column is the
output that matters: one sighting is a lead, twenty is a requirement. It is the
reason to watch many videos instead of asking a model once.

## Four traps, each of which cost a run

**AI Studio and Vertex are different billing pools.** A key for
`generativelanguage.googleapis.com` can return `429 prepayment credits are
depleted` while Vertex on the same Google account works normally. Check Vertex
before concluding you are out of quota.

**Vertex needs an explicit `role`** on each `contents` entry. Without it you get
`Please use a valid role: user, model`, which does not name the missing field.
AI Studio defaults it, so a body copied from AI Studio docs fails here.

**Vertex wants camelCase and this one fails silently.** Use `fileData`,
`fileUri`, `mimeType`. Send AI Studio's `file_data` / `file_uri` spelling and the
request returns **200 with the video dropped** — the model answers from the text
prompt alone and produces a confident, plausible paragraph about a video it
never watched. Nothing in the response says so. Always check
`usageMetadata.promptTokensDetails` for a `VIDEO` modality entry before trusting
an answer.

**`videoMetadata` is a sibling of `fileData`, not a child.** Nesting it returns
`400 Unknown name "videoMetadata" at contents[0].parts[0].file_data`.

```json
{"fileData": {"fileUri": "...", "mimeType": "video/*"},
 "videoMetadata": {"startOffset": "60s", "endOffset": "660s"}}
```

## Cost

Roughly 260 tokens per second of video, plus audio separately. Ten minutes is
about 25,000 tokens. A five-hour longplay is millions and mostly repeats what
its first ten minutes showed, so clip with offsets rather than sending whole
streams.

## Ask for structure, not prose

Pass a `responseSchema` with `responseMimeType: application/json`. A paragraph
has to be re-read by a human before it can be used; a schema gives rows you can
count, sort and turn into issues.

Include a confidence field with two values, one for what the model watched and
one for what it reasoned from a UI element or a result. Without it, observation
and inference blend into a single confident list, and the guesses are
indistinguishable from the facts. Say explicitly in the prompt that a short
honest list beats a long guessed one.

Ask what the video shows, not what the model knows. A question like "what are
this genre's mechanics" gets answered from training data whether or not the
video loaded. "What mechanics can you see happening on screen, with timestamps"
cannot be answered without watching.
