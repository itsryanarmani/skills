#!/usr/bin/env bash
# Failure cases for video-ad-check.py, written before the checker. Each bad fixture must FAIL on the named check
# and exit 1. The good fixture must exit 0. Needs ffmpeg, ffprobe, python3. Run: bash test.sh
set -u
cd "$(dirname "$0")"
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
CHECK="python3 video-ad-check.py"
PASS=0; FAILN=0

# make_video <out> <seconds> <size> <audio: voice|none|clipped|silent> <motion: yes|no>
make_video() {
  local out=$1 dur=$2 size=$3 audio=$4 motion=$5 src
  if [ "$motion" = yes ]; then src="color=c=gray:s=108x192:r=24:d=${dur},noise=alls=80:allf=t,scale=${size/x/:}"; else src="color=c=gray:s=${size}:r=24:d=${dur}"; fi
  case $audio in
    none)    ffmpeg -y -loglevel error -f lavfi -i "$src" -pix_fmt yuv420p "$out" ;;
    silent)  ffmpeg -y -loglevel error -f lavfi -i "$src" -f lavfi -i "anoisesrc=d=$dur:c=brown:a=0.003" -shortest -pix_fmt yuv420p "$out" ;;
    clipped) ffmpeg -y -loglevel error -f lavfi -i "$src" -f lavfi -i "sine=f=300:d=$dur" -af "volume=40,alimiter=limit=1" -shortest -pix_fmt yuv420p "$out" ;;
    cont)    ffmpeg -y -loglevel error -f lavfi -i "$src" -f lavfi -i "anoisesrc=d=$dur:c=brown:a=0.004" \
        -f lavfi -i "sine=f=220:d=2" -f lavfi -i "sine=f=260:d=2" -f lavfi -i "sine=f=300:d=2" \
        -filter_complex "[2:a]volume=0.5[a];[3:a]volume=0.5,adelay=2000|2000[b];[4:a]volume=0.5,adelay=4000|4000[c];[1:a][a][b][c]amix=inputs=4:normalize=0[m]" \
        -map 0:v -map "[m]" -t "$dur" -pix_fmt yuv420p "$out" ;;
    late)    ffmpeg -y -loglevel error -f lavfi -i "$src" -f lavfi -i "anoisesrc=d=$dur:c=brown:a=0.004" \
        -f lavfi -i "sine=f=220:d=1.2" -f lavfi -i "sine=f=260:d=1.2" -f lavfi -i "sine=f=300:d=1.2" \
        -filter_complex "[2:a]volume=0.5,adelay=1200|1200[a];[3:a]volume=0.5,adelay=3000|3000[b];[4:a]volume=0.5,adelay=4800|4800[c];[1:a][a][b][c]amix=inputs=4:normalize=0[m]" \
        -map 0:v -map "[m]" -t "$dur" -pix_fmt yuv420p "$out" ;;
    voice)   # three voice bursts at 0.6-1.8, 2.4-3.6, 4.2-5.4 over a quiet bed
      ffmpeg -y -loglevel error -f lavfi -i "$src" -f lavfi -i "anoisesrc=d=$dur:c=brown:a=0.004" \
        -f lavfi -i "sine=f=220:d=1.2" -f lavfi -i "sine=f=260:d=1.2" -f lavfi -i "sine=f=300:d=1.2" \
        -filter_complex "[2:a]volume=0.5,adelay=600|600[a];[3:a]volume=0.5,adelay=2400|2400[b];[4:a]volume=0.5,adelay=4200|4200[c];[1:a][a][b][c]amix=inputs=4:normalize=0[m]" \
        -map 0:v -map "[m]" -t "$dur" -pix_fmt yuv420p "$out" ;;
  esac
}

# make_manifest <out> <variant>
make_manifest() {
python3 - "$1" "$2" <<'E'
import json, sys
out, v = sys.argv[1:]
m = {
 "duration": 6.0, "size": [1080, 1920],
 "shots": [{"start": 0, "end": 1.8}, {"start": 1.8, "end": 3.6}, {"start": 3.6, "end": 6.0}],
 "voice": [{"start": 0.6, "end": 1.8, "text": "Dave went down hard"}, {"start": 2.4, "end": 3.6, "text": "That was March"}, {"start": 4.2, "end": 5.4, "text": "Still off work"}],
 "captions": [{"start": 0.6, "end": 1.8, "text": "Dave went down hard"}, {"start": 2.4, "end": 3.6, "text": "That was March"}, {"start": 4.2, "end": 5.6, "text": "Still off work"}],
 "labels": [{"text": "Dave", "start": 0.7, "end": 2.0}], "arrows": [], "allow": ["2 weeks"]
}
if v == "early": m["captions"] = [{**c, "start": c["start"] - 1.0, "end": c["end"] - 1.0} for c in m["captions"]]
if v == "arrows": m["arrows"] = [{"start": i * 1.0, "end": i * 1.0 + 1.0} for i in range(5)]
if v == "label_short": m["labels"] = [{"text": "Dave", "start": 0.7, "end": 1.1}]
if v == "long_shot": m["shots"] = [{"start": 0, "end": 4.2}, {"start": 4.2, "end": 6.0}]
if v == "gap": m["captions"] = m["captions"][:2]
if v == "number": m["captions"][2]["text"] = "50% faster"
if v == "wrongwords": m["captions"][0]["text"] = "Dave went up hard"
if v == "claim2": m["captions"][2]["text"] = "2 weeks, 99% success"; m["voice"][2]["text"] = "2 weeks 99% success"
if v == "guarantee": m["captions"][2]["text"] = "guaranteed result"; m["voice"][2]["text"] = "guaranteed result"
if v == "partial": m["captions"][0] = {"start": 0.6, "end": 1.8, "text": "Dave"}
if v == "novoice": m["voice"] = []; m["captions"] = []
if v == "cont":
    m["voice"] = [{"start": 0.0, "end": 2.0, "text": "Dave went down"}, {"start": 2.0, "end": 4.0, "text": "That was March"}, {"start": 4.0, "end": 6.0, "text": "Still off work"}]
    m["captions"] = [dict(c) for c in m["voice"]]
if v == "chunked": m["captions"][0:1] = [{"start": 0.6, "end": 0.9, "text": "Dave"}, {"start": 0.9, "end": 1.8, "text": "went down hard"}]
if v == "wordy": m["captions"][0]["text"] = "Dave went down so very hard today"
json.dump(m, open(out, "w"))
E
}

# make_cont_transcript <out>
make_cont_transcript() {
python3 - "$1" <<'E'
import json, sys
w = []
for t0, words in [(0.0, "Dave went down"), (2.0, "That was March"), (4.0, "Still off work")]:
    for i, x in enumerate(words.split()): w.append({"text": x, "start": round(t0 + 0.6 * i, 2), "end": round(t0 + 0.6 * i + 0.55, 2)})
json.dump(w, open(sys.argv[1], "w"))
E
}

# make_transcript <out> <shift seconds>
make_transcript() {
python3 - "$1" "$2" <<'E'
import json, sys
out, shift = sys.argv[1], float(sys.argv[2])
w = []
for t0, words in [(0.6, "Dave went down hard"), (2.4, "That was March"), (4.2, "Still off work")]:
    for i, x in enumerate(words.split()): w.append({"text": x, "start": round(t0 + 0.3 * i + shift, 2), "end": round(t0 + 0.3 * i + 0.28 + shift, 2)})
json.dump(w, open(out, "w"))
E
}

expect() { # expect <name> <fail|pass> <check name or -> <cmd...>
  local name=$1 want=$2 chk=$3; shift 3
  local outp; outp=$("$@" 2>&1); local rc=$?
  if [ "$want" = pass ]; then
    if [ $rc -eq 0 ]; then PASS=$((PASS+1)); echo "ok   $name"; else FAILN=$((FAILN+1)); echo "FAIL $name (expected pass, rc=$rc)"; echo "$outp" | grep -E "^FAIL|NOTE"; fi
  else
    if [ $rc -ne 0 ] && echo "$outp" | grep -q "FAIL $chk"; then PASS=$((PASS+1)); echo "ok   $name"; else FAILN=$((FAILN+1)); echo "FAIL $name (expected FAIL $chk, rc=$rc)"; echo "$outp" | grep -E "^FAIL|NOTE"; fi
  fi
}

make_video "$T/good.mp4" 6 1080x1920 voice yes
make_manifest "$T/good.json" good
make_transcript "$T/good-tr.json" 0

python3 - "$T/quirk-tr.json" <<'E'
import json,sys
w=json.load(open(sys.argv[1].replace("quirk","good")))
w[0]["start"]=0; w[0]["end"]=0.1
json.dump(w,open(sys.argv[1],"w"))
E
expect "good video passes"                      pass -            $CHECK "$T/good.mp4" --manifest "$T/good.json" --transcript "$T/good-tr.json"
make_manifest "$T/early.json" early
expect "first-word quirk in the transcript still passes" pass - $CHECK "$T/good.mp4" --manifest "$T/good.json" --transcript "$T/quirk-tr.json"
expect "captions one second early fail sync"    fail sync-manifest $CHECK "$T/good.mp4" --manifest "$T/early.json"
make_manifest "$T/arrows.json" arrows
expect "five arrows fail overlay density"       fail overlay-density $CHECK "$T/good.mp4" --manifest "$T/arrows.json"
make_manifest "$T/ls.json" label_short
expect "label on screen 0.4 s fails hold"       fail label-hold   $CHECK "$T/good.mp4" --manifest "$T/ls.json"
make_manifest "$T/long.json" long_shot
expect "a 4.2 s shot fails cut pace"            fail cut-pace     $CHECK "$T/good.mp4" --manifest "$T/long.json"
make_video "$T/still.mp4" 6 1080x1920 voice no
expect "static first 2 s fails hook"            fail hook-motion  $CHECK "$T/still.mp4" --manifest "$T/good.json"
make_video "$T/noaudio.mp4" 6 1080x1920 none yes
expect "no audio stream fails"                  fail audio-present $CHECK "$T/noaudio.mp4" --manifest "$T/good.json"
make_video "$T/small.mp4" 6 540x960 voice yes
expect "wrong size fails"                       fail size         $CHECK "$T/small.mp4" --manifest "$T/good.json"
make_video "$T/silent.mp4" 6 1080x1920 silent yes
expect "voice missing in its window fails"      fail voice-present $CHECK "$T/silent.mp4" --manifest "$T/good.json"
make_video "$T/clip.mp4" 6 1080x1920 clipped yes
expect "clipped audio fails level"              fail audio-level  $CHECK "$T/clip.mp4" --manifest "$T/good.json"
make_manifest "$T/gap.json" gap
expect "spoken line with no caption fails mute" fail mute-coverage $CHECK "$T/good.mp4" --manifest "$T/gap.json"
make_manifest "$T/num.json" number
expect "unallowed number in caption fails"      fail claims       $CHECK "$T/good.mp4" --manifest "$T/num.json"
make_manifest "$T/wordy.json" wordy
expect "caption over 6 words fails"             fail caption-length $CHECK "$T/good.mp4" --manifest "$T/wordy.json"
make_transcript "$T/late-tr.json" 1.0
expect "transcript one second late fails sync"  fail sync-transcript $CHECK "$T/good.mp4" --manifest "$T/good.json" --transcript "$T/late-tr.json"
make_video "$T/late.mp4" 6 1080x1920 late yes
expect "voice 0.6 s later than the manifest fails onset" fail voice-onset $CHECK "$T/late.mp4" --manifest "$T/good.json"
make_manifest "$T/ww.json" wrongwords
expect "captions with wrong words after the first fail transcript" fail sync-transcript $CHECK "$T/good.mp4" --manifest "$T/ww.json" --transcript "$T/good-tr.json"
expect "no transcript fails, it is never skipped" fail sync-transcript $CHECK "$T/good.mp4" --manifest "$T/good.json"
make_manifest "$T/c2.json" claim2
expect "allowed phrase plus an unconfirmed number fails claims" fail claims $CHECK "$T/good.mp4" --manifest "$T/c2.json" --transcript "$T/good-tr.json"
make_manifest "$T/gu.json" guarantee
expect "guaranteed fails claims" fail claims $CHECK "$T/good.mp4" --manifest "$T/gu.json" --transcript "$T/good-tr.json"
make_manifest "$T/pa.json" partial
expect "one word held over a longer line fails coverage" fail mute-coverage $CHECK "$T/good.mp4" --manifest "$T/pa.json" --transcript "$T/good-tr.json"
make_manifest "$T/nv.json" novoice
expect "a manifest with no voice and not muted fails" fail voice-present $CHECK "$T/good.mp4" --manifest "$T/nv.json" --transcript "$T/good-tr.json"
make_video "$T/cont.mp4" 6 1080x1920 cont yes
make_manifest "$T/cont.json" cont
make_cont_transcript "$T/cont-tr.json"
expect "continuous speech with no gaps passes onset" pass - $CHECK "$T/cont.mp4" --manifest "$T/cont.json" --transcript "$T/cont-tr.json"
python3 - "$T/extra-tr.json" <<'E'
import json, sys
w = json.load(open(sys.argv[1].replace("extra", "good")))
w.insert(1, {"text": "never", "start": 0.75, "end": 0.9})
json.dump(w, open(sys.argv[1], "w"))
E
make_manifest "$T/chunk.json" chunked
expect "chunked captions pass with the real transcript" pass - $CHECK "$T/good.mp4" --manifest "$T/chunk.json" --transcript "$T/good-tr.json"
expect "a spoken word the captions skip between chunks fails transcript" fail sync-transcript $CHECK "$T/good.mp4" --manifest "$T/chunk.json" --transcript "$T/extra-tr.json"
expect "unreadable manifest fails loudly"       fail manifest     $CHECK "$T/good.mp4" --manifest "$T/does-not-exist.json"

echo "$PASS passed, $FAILN failed"
[ "$FAILN" -eq 0 ]
