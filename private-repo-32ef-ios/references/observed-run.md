# Observed run

One run on one phone. It is a single data point.

## Setup

- iPhone 12 Pro Max, iOS 27.0.1, Display Zoom on, so WDA reported 375 by 812.
- Map: `iphoneX` (375 by 812).
- Task: TikTok `doomscroll`, `casual`, 3 minutes, likes and saves off.
- No passcode stored.

## Result

The run failed. The last log line:

```text
Finished doomscroll: videosViewed=3 swipes=3 likes=0 saves=0 comments=0 recoveries=3 elapsedMs=112218 reason=stopped
```

- TikTok opened and the farm read the feed.
- Three times the screen read as `springboard`. The farm relaunched TikTok each time.
- The farm often read the For You feed as `following`. It tapped the For You tab again.
- The log ended with `Could not recover to For You feed after identify/relaunch attempts`.
- A stop was sent after 112 seconds. The phone was on the home screen with a folder open.

## What this does and does not show

- It shows the farm can open TikTok and read the screen on a real iPhone.
- It does not show why the screen fell back to the home screen. The likely cause is the mismatch between the zoomed screen and the map. That is a guess.
- A locked phone also reads as the home screen. Auto-Lock and a stored passcode can matter.

## Next test

Turn Display Zoom off. Try the `iphone13` map. Record `videosViewed`, `swipes` and `recoveries` for the same 3-minute task. Add the result here.
