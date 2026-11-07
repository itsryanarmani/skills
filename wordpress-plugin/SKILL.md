---
name: wordpress-plugin
description: "Use when building, testing or submitting a WordPress plugin that is a thin PHP client over your product's REST API: settings page, metabox, wp-env, zipping, and WordPress.org review rejections."
---

# Building a WordPress plugin

A WordPress plugin is **plain PHP with a header-comment manifest** — no build step, no framework SDK. The main file's header block (`Plugin Name`, `Version`, `Text Domain`, …) IS the manifest WordPress reads. Source lives in `integrations/wordpress-plugin/`. It is a thin frontend over your own public REST API: WordPress hooks supply the events (`save_post`, settings pages, editor metaboxes); `wp_remote_request` calls your API with the user's own team API key. Read this before the first file; the command-level playbook is in `itsryanarmani/scripts` `scripts/wordpress-plugin/README.md`.

## When to use

- **Triggers:** 'build a WordPress plugin', 'submit a plugin to wordpress.org', 'plugin review rejected', 'readme.txt stable tag', 'plugins.svn.wordpress.org trunk tags', 'wp_remote_request', 'nonce verification', 'wp-env'.
- Reviewers grep every $_POST/$_GET for nonce, capability and sanitize (the top rejection); escape output late.
- readme.txt 'Stable tag' must equal the header Version and a real SVN tag; plugin-page assets live in SVN /assets, not trunk; the folder and text domain must match the approved slug. Each review round costs days to weeks.
- Siblings: canva-app, zapier-integration, browser-extension, figma-plugin, connector-directory-submission.

## The trap that wastes a week: review greps every `$_POST`, and each bounce re-queues you for days

WordPress.org review is **manual** — a volunteer reads your code, and every rejection puts you back in a days-to-weeks queue. The #1 bounce cause is **a `$_POST` / `$_GET` / `$_REQUEST` read without the full guard triplet**:

1. **Nonce** — `wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['your_nonce'] ) ), 'your_action' )` for forms; `check_ajax_referer()` for AJAX.
2. **Capability** — `current_user_can( 'manage_options' )` for settings, `current_user_can( 'edit_post', $post_id )` for metabox saves.
3. **Sanitize in, escape out** — `sanitize_text_field` / `sanitize_key` / `absint` on input; `esc_html` / `esc_attr` / `esc_url` at the `echo`, not at assignment. `wp_unslash()` BEFORE sanitize — WordPress magic-quotes superglobals, so sanitizing a slashed value is both a bug and a PHPCS flag.

The Settings API is the one free pass: `register_setting` + `settings_fields()` supplies the nonce for you — but the `sanitize_callback` is still mandatory. A hand-rolled `<form>` that skips `settings_fields()` is a nonce-less `$_POST` handler, and that is a bounce.

**Rule: run `phpcs --standard=WordPress` before you zip.** Reviewers run the same greps; PHPCS is the only pre-flight that catches triplet violations before they do.

## The other traps that each cost a round-trip

1. **`Stable tag` = header `Version` = an existing SVN tag.** readme.txt `Stable tag: 1.0.0` must match the main file's `Version:` AND `tags/1.0.0` must exist in SVN. Point at a missing tag and the directory serves the wrong code — or nothing.
2. **Plugin-page assets live in `/assets`, NOT in trunk.** Icons (`icon-128x128.png`, `icon-256x256.png`), banners (`banner-772x250.png`), and screenshots sit in a top-level `/assets` dir next to `trunk/` and `tags/`. Committed into trunk, they never render on the plugin page.
3. **Folder, text domain, and slug must match the APPROVED slug.** You request a slug on upload; if it's taken they assign another. Then the zip's folder name, `Text Domain`, and every prefix must be renamed to match — a mismatch bounces. Names/slugs that start with someone else's trademark also bounce.
4. **No remote code, no bundled secrets, no silent telemetry.** Calling your documented API with a user-supplied key is fine. Loading JS/CSS from a CDN, `eval`, ionCube/obfuscated or minified-only JS, and phoning home without consent are guideline violations (instant reject). The API key lives in the site's options table, never in the zip.
5. **Prefix everything; guard every file.** All functions/classes/options/meta keys get a unique prefix, and every PHP file starts with `defined( 'ABSPATH' ) || exit;`. Generic names collide with other plugins — reviewers reject for it.
6. **`uninstall.php` must clean up** — delete the plugin's options and post meta. Reviewers check.
7. **Enqueue, never hardcode.** Scripts and styles load via `wp_enqueue_script()` / `wp_enqueue_style()` with `plugins_url()` — a hardcoded `<script>` tag or CDN link in a settings page gets flagged (and the CDN link doubles as a remote-code violation).
8. **AJAX handlers must end in `wp_die()`.** An `admin-ajax.php` callback that returns normally prints a trailing `0` and corrupts every JSON response — looks like your API is broken, but it's the handler.

Also: `save_post` fires on autosaves and revisions — bail on `wp_is_post_autosave()` / `wp_is_post_revision()` and guard against re-entrancy before calling your API, or every keystroke spams it. And a **scheduled** post going live (future → publish, via cron) does not reliably re-enter `save_post` with `publish` — hook `transition_post_status` too, or scheduled posts silently never sync.

## readme.txt is a second manifest (and reviewers read it first)

The PHP header names the plugin to WordPress; `readme.txt` feeds the entire directory page, the updater, and wp-admin plugin search. The fields that bite:

- **Header block** — `Contributors` (real wordpress.org usernames), `Tags` (max 5), `Requires at least`, `Tested up to` (≤ the current WP release: a future version warns, a stale one sinks search rank), `Stable tag`, `Requires PHP`, `License` (must be GPL-compatible).
- **The short description under the header is the search snippet** — one sentence, ~150 chars. It is all the directory card and wp-admin search show.
- **`== Screenshots ==` is positional** — list item N renders `assets/screenshot-N.png` from SVN `/assets`; a caption with no matching file shows a broken image on the plugin page.
- **`== Changelog ==` entries must match tagged versions** — the update notice pulls from here; no entry for the current tag makes the plugin look abandoned.

## Build path

- No build step: PHP files + readme.txt. Test locally with `@wordpress/env` (`npx wp-env start`, maps the folder as a plugin via `.wp-env.json`) or rsync/symlink into any site's `wp-content/plugins/<slug>/`.
- Settings: the **Settings API** (`register_setting` with a `sanitize_callback`) — one array option, autoload-safe. HTTP: **`wp_remote_request` / `wp_remote_post`** (the WordPress HTTP API), never raw `curl` or `file_get_contents` — WPCS flags both.
- Keep all business logic server-side in your product; the plugin is a thin client: hook event → build payload → `POST` with `Authorization: Bearer <team API key>` → surface `WP_Error` in the admin, don't swallow it.
- The usual lifecycle mapping: first publish → `POST` create on your API, later update → `PATCH`, permanent delete → `DELETE`, a settings-page "Test connection" button → a cheap `GET`. Store the remote ID in post meta so updates patch instead of duplicating.
- Every user-facing string goes through `__( ..., '<slug>' )` with the text domain, loaded via `load_plugin_textdomain()` on `init` — wordpress.org auto-translates listed plugins, and untranslatable strings get flagged.
- Pre-flight: `composer global require wp-coding-standards/wpcs`, then `phpcs --standard=WordPress .`

## Submission — WordPress.org plugin directory

**Bucket: manual review, free.** Steps:
1. Zip the folder (respect `.distignore`: no `node_modules`, tests, `.env`, zips). The folder inside the zip must be named `<slug>/`.
2. Log in at `login.wordpress.org`, open `wordpress.org/plugins/developers/add/`, upload the zip, request your slug. `Contributors:` in readme.txt must be real wordpress.org usernames.
3. Wait for the review email (days–weeks). **Do not touch SVN before approval** — the repo doesn't exist yet. **Approval ≠ listed:** nothing appears until you do the SVN import below; review happened on the zip, hosting is SVN.
4. On approval: `svn checkout https://plugins.svn.wordpress.org/<slug>/`, rsync the source into `trunk/`, `svn add trunk --force`, `svn ci`.
5. `svn cp trunk tags/1.0.0 && svn ci` — required so `Stable tag` resolves. Commit `/assets` (icons/banners/screenshots) separately at the repo root.
6. Later releases: bump `Version` AND `Stable tag`, add a `== Changelog ==` entry, rsync → trunk, commit, tag again. No re-review for routine updates.

Review feedback arrives by email from the plugins team. Fix what they flag, re-zip, re-upload at the same `/developers/add/` URL, and reply on the same thread — resubmitting as a new plugin restarts the queue from zero.

**Submittable: portal-review** (manual zip review, then SVN self-host — no publish API). **Plugin-page assets** live in SVN `/assets` (sibling of `trunk/`, never in trunk): icon `128×128` + `256×256` PNG, banner `772×250` + `1544×500`, and `screenshot-N.png` files referenced by caption in readme.txt. No developer fee, no OAuth registration; the only gate is a real `login.wordpress.org` account whose username is in `Contributors:`.

**Silent-bounce gotchas:** the nonce/sanitize/escape triplet (above); `Stable tag` pointing at a missing tag; a plugin name starting with another's trademark; minified-only JS; anything phoning home on install. Review-queue length is variable and unpublished (days–weeks); assume slow.

## Parity checklist (prove on a real WP site before zipping)

activate without warnings · save settings (key persists; blank keeps the old one) · publish a post and see the API call land · a `WP_Error` surfaces as an admin notice · per-post skip/override works · uninstall removes all options/meta · `phpcs --standard=WordPress` is clean.

## Related skills

- `zapier-integration` — the same "thin client over your REST API" shape on Zapier's CLI; the auth-wiring lesson rhymes.
- `canva-app` — another marketplace where a reviewer must succeed from a clean, no-account state.
- `connector-directory-submission` — the cross-marketplace submission router.
