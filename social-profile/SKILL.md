---
name: social-profile
description: Set the profile picture, cover and bio on many social networks with the social-profile CLI. Load when the user wants to update an avatar, profile photo, cover, header, banner or bio on X, Bluesky, Mastodon, GitHub, Reddit, YouTube, Instagram, LinkedIn, TikTok, Facebook, Pinterest or Tumblr, one platform or all of them at once.
---

# Social profile

One command sets the avatar, banner and bio on many platforms. API platforms use
tokens. Browser platforms drive a Playwright profile the user has already signed in to.
Images are center-cropped to each platform's aspect ratio, then resized.

Tool: `social-profile` in pooriaarab/scripts. Docs: `social-profile.md` in the same repo.
Source PR: https://github.com/pooriaarab/scripts/pull/728

## Install

```sh
gh api repos/pooriaarab/scripts/contents/social-profile -H "Accept: application/vnd.github.raw" > ~/.local/bin/social-profile
chmod +x ~/.local/bin/social-profile   # add ?ref=scr-727-social-profile until PR #728 merges
pip install pillow                                        # required
pip install playwright && playwright install chromium     # only for browser platforms
```

## Credentials

- Put tokens in env vars, or in `~/.config/social-profile/config.toml` with mode `0600`.
  Env vars win. `SOCIAL_PROFILE_CONFIG` overrides the path. The tool refuses a file that is not `0600`.
- Never print, paste or commit a token or the config file.
- Bluesky takes an app password. Never the main password.
- Never type a password into a browser flow. The user signs in by hand.

## Steps

1. Run `social-profile list`. It shows each platform, its method, its fields and its env vars.
2. Dry-run first. It writes the resized images, checks the bio length and makes no network calls.

   ```sh
   social-profile set --platform all --avatar me.png --banner wide.png --bio "Builder." --dry-run
   ```

3. Run the same command without `--dry-run`. Use one platform name or `all`.
4. Read the result. `all` prints `OK`, `SKIP` or `FAIL` per platform and exits 1 if any fail.
   Report each line to the user. Do not call a run done while a line says `FAIL`.

## Platforms

| Platform | Method | Avatar | Banner | Bio limit |
|---|---|---|---|---|
| x | api | yes | yes | 160 |
| bluesky | api | yes | yes | 256 |
| mastodon | api | yes | yes | 500 |
| github | api | no API | none | 160 |
| reddit | api, unverified | browser only, not automated | browser only, not automated | 200 |
| youtube | api | no API | yes | 1000 |
| instagram | browser | yes | none | 150 |
| linkedin | browser | yes | yes | 220 (headline) |
| tiktok | browser | yes | none | 80 |
| facebook | browser | yes | yes | 101 |
| pinterest | browser | yes | yes | 500 |
| tumblr | browser, unverified | yes | yes | 500 |

Where a field is not supported, tell the user to change it by hand on the site.
Tumblr also needs `TUMBLR_BLOG`. YouTube's access token expires after an hour.

## Browser platforms

They need a browser profile that is already signed in. Pass `--browser-profile <dir>`
or set `SOCIAL_PROFILE_BROWSER_PROFILE`. The tool does not wait for a login. To sign in,
open the same profile dir and let the user log in by hand, then close the window:

```sh
playwright open --user-data-dir ~/.cache/sp-chrome https://www.instagram.com/accounts/login/
social-profile set --platform instagram --avatar me.png --browser-profile ~/.cache/sp-chrome
```

Add `--headful` to watch a run.

These flows are best-effort. Selectors may break when a site changes. Fixes go in the
`BROWSER` dict in the script.

## When it fails

- "not signed in in this browser profile": stop. Have the user sign in to that profile dir as above, then rerun.
- Bio too long: the platform shows `FAIL`. Never truncate the bio silently. Show the limit,
  propose a shorter bio and get the user's approval.
- `SKIP not configured: set ...`: in an `all` run, unconfigured platforms are skipped.
  A named platform with missing credentials is a `FAIL`. Tell the user which env vars to set.
- A broken selector: report the platform and the step. Do not retry in a loop.
