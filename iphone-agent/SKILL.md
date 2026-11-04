---
name: iphone-agent
description: "Use when driving the owner's iPhone through esp32-iphone-agent, UxPlay name iPhone Agent, and an ESP32-S3 USB HID mouse on AssistiveTouch."
---

# iPhone agent

Drive the owner's iPhone through esp32-iphone-agent. The mirror name is iPhone Agent. The input is an ESP32-S3 USB HID mouse on AssistiveTouch.

## References

Read the file that fits the task:

- [Setup](references/setup.md) — phone settings, cable roles, and radio limits.
- [Devices](references/devices.md) — ports, iOS limits, and the proof rule.
- [Calibration](references/calibration.md) — span measure and the center check.
- [API](references/api.md) — HTTP routes, board lines, and error codes.
- [Recipes](references/recipes.md) — only steps a frame has shown.
- [Messages](references/messages.md) — open the list, then leave.
- [Safari](references/safari.md) — open the browser, then leave.
- [Phone](references/phone.md) — open Calls, then leave.
- [Dock folder](references/t3.md) — the Productivity folder holds T3 Code and Muse.
- [Settings](references/settings.md) — open Settings, then leave.
- [Mail](references/mail.md) — open Mail, then leave.
- [Notifications](references/notifications.md) — open Notification Centre, then leave.
- [Facebook](references/facebook.md) — open Facebook, then leave.
- [Instagram](references/instagram.md) — open Instagram, then leave.
- [TikTok](references/tiktok.md) — open TikTok, then leave.
- [X](references/x.md) — open the Chat screen, then leave.
- [LinkedIn](references/linkedin.md) — open LinkedIn, then leave.
- [Camera](references/camera.md) — open Camera from App Library. Do not press the shutter.
- [Warmup](references/warmup.md) — social media account warmup across Instagram, TikTok, X, LinkedIn, YouTube.
- [Instagram signup](references/instagram-signup.md) — create an account: screens, order, gotchas, stop points.
- [Send to iPhone](references/send-to-iphone.md) — put a file in the phone's Photos or mail.

## Gates

- Do one named action.
- **Warmup scripts** override the interaction gates below (they perform likes, comments, DMs, follows intentionally). The gates remain for one-off manual tasks.
- Stop before send, post, comment, like, share, follow, call, pay, delete, sign-in, password, erase, or a permission grant (unless called via `warmup-*` scripts).
- Read the frame after every gesture. The first frame can still show the old screen. Wait, then save again, before you call the gesture a miss.
- A click in the dark area leaves the app switcher onto the screen behind it. That screen can be the home screen, an open folder, or App Library.
- Do not loop a feed.
- The pointer is AssistiveTouch and apps can see it.
- Do not restart the server.
- Stay off the AssistiveTouch button.
- Raw `home` only parks the pointer. Do not trust a home swipe until the frame shows the home screen. A slow drag from the bottom opens the app switcher.
- A full iPhone is not claimed until the round pointer moves on that phone.
- Prove the screen source is live before an action: wiggle the pointer and expect a new frame. A still screen writes no frames, so frame age alone proves nothing. A dead AirPlay mirror produced minutes of blind moves.
- Never press when the pointer ring was seen before and is not on the target. USB frames (`usbcap`) do not drop under load and are stretched, so the ring is an ellipse.
- The Home route is the AssistiveTouch button, then its Home icon. Edge swipes and the board's Home click did nothing on the test phone.

## Scope

- Send storage questions to org-iphone-storage.
- Some3C and Novatek boards are out of scope.
