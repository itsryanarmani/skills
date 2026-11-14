# Live learnings (iPhone 12 Pro Max, iOS 27 beta)

Each item says how sure we are. "Seen" means it happened on the phone. "Not tested" means it is a guess.

## Screenshots are cut off (seen)

- The phone screen is 428x926 points. WDA says so at `/window/size`.
- The WDA and Appium screenshot is 1124x2436 pixels. That is the top-left 375x812 points at 3x.
- The right side and the bottom 114 points are missing. The like, comment and share icons are in the missing part. The tab bar is missing too.
- The farm checks for a dark tab bar in the bottom 10% of the image. It finds none. It reports "springboard" with 0.90 confidence while TikTok is in front.
- Proof: the Settings icon sits at x=326 points in the WDA element tree. It appears at about 329 points in the screenshot. So the scale is 3x, and the image is a crop.
- A `UILaunchScreen` key in the runner `Info.plist` did **not** fix it. Do not repeat that.
- The repo's `iphoneX` profile is 375x812. A phone in Zoomed mode matches it, and a screenshot is then whole. Not tested: Zoomed mode. On this iOS version the Display & Brightness page had no Display Zoom row.
- Result: without a fix, the farm cannot read the screen in Default mode.

### Fix that worked (seen)

- `getScreenshot` in `src/devices/wda-remote.ts` now pads the cropped image with black to the true screen size (1284x2778 px here). It does nothing for a full-size image.
- With the padding, the tab-bar and SpringBoard checks see the proportions they expect. The "springboard" mistake went away.
- The TikTok header on this phone has more tabs (LIVE, Community, Nearby, Following, For You). The old band for "For You" (58 to 74% of the width) covered "Following". `detectHomeFeedTab` now also checks 75 to 87%. A visible header tab now counts as proof of the feed.
- The right-hand icon rail (like, comment, share) stays outside the capture. The farm uses fixed seeds for it. Not tested: whether those seeds hit the icons. Do not turn on likes, saves or comments until you check them by hand.
- `private-repo-32ef doctor <udid>` reports CROPPED or OK. `private-repo-32ef apply-patch` applies all of these farm fixes.

## Launching TikTok (seen)

- WDA and Appium `activateApp` return "foreground" (state 4) while SpringBoard stays on screen.
- `xcrun devicectl device process launch --device <udid> [--terminate-existing] <bundleId>` opens the app every time.
- The farm now launches with `devicectl` (`src/devices/devicectl.ts`) and sets `appium:autoLaunch: false`.

## Do not poke WDA while a run is active (seen)

- A second WDA session created by hand ends the farm's Appium session. The run then fails with "Session does not exist".
- Use the farm routes instead: `/api/devices/<udid>/remote/screenshot` and `/remote/action`.

## Do not read the page source of TikTok (seen)

- `GET /source` on the TikTok feed hangs, and WDA then stops. The supervisor restarts it in about 30 seconds.
- Read icon positions from screenshots. Read the element tree only in Settings and SpringBoard.

## Other apps on the phone (seen)

- A "back to TikTok" link in the status bar led to another app, and the next back led to a third. Do not tap the back link. Launch the target app with `devicectl`.
- Never send taps while a personal app is in front. One screen had a "Switch recorder off" button.
- An Exchange account alert ("Password Incorrect") can appear over Settings. Tap Cancel. Never type a password.

## Wi-Fi (seen)

- Taps, swipes and screenshots work over Wi-Fi while WDA runs.
- The WDA supervisor starts WDA only for a USB phone. After a crash, plug the cable in once.

## Result of the first good run (seen)

- 3-minute passive run: likes, saves and comments off. Outcome: `videosViewed=6 swipes=6 recoveries=0`. All 7 screen reads said "fyp".
- Before the fixes, every run ended with "Could not recover to For You feed" and 0 videos.
- This shows the farm works. It does not show that TikTok cannot detect it.

## Human-like input (done, not yet shown to help)

- The old swipe was one straight line: same X, same start and end, same time, 40 ms hold.
- `src/tiktok/human-gesture.ts` builds a curved stroke with 9 to 12 points. The speed rises then falls. The start, end, drift and total time vary. The finger rests 30 to 140 ms before it moves. One swipe in eight pauses mid-stroke.
- The wait after a swipe now follows a log-normal curve, not a flat 550 to 800 ms range.
- Touch pressure is not set. XCTest touches carry no force on this phone.
- Not tested: whether TikTok can tell the difference. Treat the change as less obvious, not as safe.

## TikTok rail positions on a 428x926 phone (iPhone 12 Pro Max)

The WDA screenshot crops the right rail, so find icons by tapping, not by eye.
Tested with W3C touch actions (428x926 pt, TikTok For You feed):

| Icon | Point (x, y) | Result |
|---|---|---|
| Search (top right) | 402, 69 | Search page opened, keyboard up |
| Comment | 397, 585 | Comments sheet opened |
| Share | 397, 722 | Share sheet opened |
| Like | about 397, 518 | Not tested. Inferred from the 67 pt rail spacing |
| Save | about 397, 654 | Not tested. Inferred from the same spacing |

- The farm tap API refuses x above its profile width (390 for `iphone13`). Use
  WDA actions directly, or add a 428x926 profile, for rail taps.
- Close a sheet by relaunching with `devicectl`. Do not tap back links.
- Have a Haiku subagent read the screenshots. It answers "which screen is
  this" for a small token cost.

## Tested action flows (`scripts/tiktok_actions.py`)

| Flow | Steps that worked |
|---|---|
| Comment | tap comment (397, 585), tap composer (150, 896), type, tap send (402, 583). Comment showed first, 1 s old. |
| Share | tap (397, 722). Share sheet opens. Close it with `launch`. |
| Search | tap (402, 69). The search page opens with the keyboard. Type, then return. |
| Next video | swipe up from (130, 700) to (136, 200), 380 ms, with the human gesture. |
| Like, save | Taps sent. State cannot be seen: the rail is outside the screenshot. Double-tap on the video did not show a heart burst either. Check in the app by hand before you trust them. |

Traps found on the way:
- Python `urllib` calls to WDA get truncated bodies (`IncompleteRead`, `RemoteDisconnected`). Use `curl`.
- WDA `/screenshot` often returns a truncated body. Use the farm screenshot API.
- The send button and the rail sit past x=375, so no screenshot shows them. Find them by tapping.
- The comment sheet composer sits at y about 896, below the crop. Tap it blind.

## Result with the 428x926 profile (iPhone 12 Pro Max)

A 3-minute farm run with likes and saves on: 12 videos, 7 likes, 3 saves, 1 live
skipped, 0 recoveries. Set `coordinateProfile` to `iphone12promax`.

- The farm profile uses the tapped rail points: like (397, 518), comment (397, 585),
  save (397, 654).
- Saves landed. The profile Favorites tab (bookmark icon) shows 9+ videos. It can
  hold older saves, so the count does not prove all 3.
- Likes are not confirmed. The Liked tab (heart) sat under the AssistiveTouch button.
- The bottom tab bar is at y=884, not the scaled y=911. Tap profile at (386, 884).
- On the profile page the bookmark tab is at (264, 293) and the heart tab at (363, 293).
- 7 likes in 12 videos is a 58 percent like rate. Use a low rate on a real account.
