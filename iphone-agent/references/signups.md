# Social signups

How to create accounts on an iPhone with the pointer board. Verified on a real iPhone (iOS 27) on 2026-11-04 and 2026-11-05. Full step tables live in the phone-farm repo under `docs/`, one page per app. `pf app list` shows the scripted flows.

## Rules for every signup

- Make the password on the Mac. Save it in the login Keychain. Read it back before you type it. Never print it.
- Use one Gmail address for every app. Read email codes from the Gmail app on the phone.
- Do not tap suggested emails or saved logins. They belong to other accounts.
- A passkey prompt needs Face ID. Close it.
- Skip contacts, phone number, Facebook search and follow suggestions.
- Set the name and the photo before you leave the app.

## Per app

| App | Route | Gotcha |
|---|---|---|
| Gmail | Settings > Add account > Create | No phone number and no typed password. iOS makes the password |
| Instagram | Profile > account switcher > Add account > Create | Choose "email" to keep it out of the Accounts Center. Birthday is a wheel |
| TikTok | Profile > Add account > email | Username is locked for 30 days. Birthday is a wheel. Spotlight can open the wrong app: check the screen |
| YouTube | Avatar > Create a channel | Uses the Google account. No new password. Do not tap the pencil under the AssistiveTouch button |
| Threads | Settings > Switch profiles > Add profile > Join using your Meta Account | Name, photo and handle come from Instagram |
| Reddit | Profile > account switcher > Add account > email | The username is permanent. Orange buttons hide the pointer unless the ring filter is tight |
| Medium | Chrome > `medium.com/m/signin?operation=register` > email | No password: an emailed code. Safari private tabs need Face ID and normal tabs stop at 500. Use Chrome |

## No add-account route

Snapchat and Discord have only Log Out. Telegram needs a phone number. Pinterest returned "Invalid parameters" at the birthdate step. Skip them unless the owner agrees to log out.

## Pointer and typing gotchas

- Right-click is Home (1.6 s). Middle-click is the App Switcher. Set `mouse_buttons: true` for the phone.
- A target inside the AssistiveTouch zone (x 0.83 to 1.0, y 0.48 to 0.57) needs `move_to_px` then `click`.
- The ring is pink-red (248, 56, 48). Red and orange buttons break a loose colour filter.
- The page moves when the keyboard opens. Tap a field, wait, then type. Use Tab to reach the next field.
- Fast typing drops a character. For a code, type one digit per call with a 0.7 s wait.
- OCR cannot read small date-wheel digits. Ask the vision model for the day column.
- `scroll` can fail on a web page. Use a swipe.
- If the screen stops updating, restart the USB capture from a shell. It dies under load.
