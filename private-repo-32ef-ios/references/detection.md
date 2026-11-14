# Detection

Status: **untested**. Nobody ran this farm against a ban. This page is a reading of the code and of how the platforms work. Treat it as risk, not fact.

## What the platforms can see

| Layer | Risk | Why |
| --- | --- | --- |
| Device | Low | A real iPhone runs the real app. Touches come from the XCTest framework. There is no emulator, no jailbreak and no injected code. |
| Device state | Unknown | Developer Mode is on, and WDA runs as a second app. It is not known if TikTok or Instagram read either. |
| Behavior | The main risk | See below. |
| Account | High for DMs | Cold DMs and mass follows are the usual cause of a flag or a ban. |
| Terms | Certain | Both platforms prohibit automation. A ban needs no detection if the account is reported. |

## Behavior signals

The code adds random delay. Swipe pauses run about 350 to 800 ms, and likes and saves are drawn at random. It is not a fixed script. Still, platforms look at patterns over days:

- The same hours, the same session length and the same flow every day.
- Many accounts on one phone, one IP or one Apple ID.
- A new account with a high action rate.
- Volume of DMs, follows and comments.

## Rules for a test

- Use a throwaway account. Do not use the owner's real account.
- Start with watch-only scrolling. Keep likes, saves and comments off.
- Add one action type at a time. Record the date and the result.
- Do not run cold DMs on any account you want to keep.
- Say plainly in any report that detection was not measured.
