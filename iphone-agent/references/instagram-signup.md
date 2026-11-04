# Instagram signup

Create an Instagram account from the Instagram app on a phone that is signed in to another account.
The flow ran on a real iPhone on 2026-11-04. It lives in phone-farm as `pf app instagram signup`
(`docs/instagram-signup.md` there has every coordinate). The packaged function has not run end to
end. Each stage ran.

**Stop point:** this creates an account and accepts Instagram's terms. Run it only when the owner asked
for that account. Stop at a captcha, a selfie video or a phone-number demand. A person finishes that page.

## Order of screens

1. Profile of the signed-in account, then the username header, then "Add Instagram account", then "Create new account".
2. Create a username. Replace the suggestion. A green check beside the box means the name is free.
3. Accounts Center. Choose "Use mobile number or email". "Allow and continue" links the new account to the
   other accounts on the phone and shares ads data.
4. Create a password. Type it. The screen shows no dots to a vision model, so confirm from the next screen.
5. Birthday. Three wheels. Set the year first, then the month, then the day. Tap a row within 3 of the value,
   flick for a farther one, and read the value after every move.
6. Mobile number. The box holds the phone's own number. Choose "Sign up with email".
7. Email. The box holds the owner's main address. Replace it.
8. Confirmation code. Read it in the Gmail app, return, type it into the first box. The signup survives the trip.
9. Terms. "I agree" is below the fold on a small frame. Find it by OCR.
10. Optional pages: picture, settings review (turn contacts sync off), Facebook search (a popup asks to confirm
    the skip), name and bio, phone, follow list, interests. Skip each. Stop when the tab bar shows.

## Gotchas

- Typing reaches password fields. The Passwords app's New Password form did not show typed text and offers
  no strong-password bar, because the board is a hardware keyboard and iOS shows no software keyboard.
- Home: the board's Home click and edge swipes did nothing. Press the floating AssistiveTouch button with the
  pointer (a normal tap must dodge it), then its Home icon.
- Open an app from Spotlight by tapping the top hit. Enter opened the wrong app.
- Gmail opens on the last account used. Switch with the avatar menu. A tap near the top right can star a message.
- Notifications: Instagram offers only a 15-minute or 8-hour pause. Switch each category off one by one.
- A vision model reading masked dots said a full field was empty. Reveal and count with OCR when it matters.
- Frames go to the vision model. A picker or inbox shows other people's data.
