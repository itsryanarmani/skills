---
name: social-provider-qualification
description: "Qualify one Content Rabbit social provider for production: provider approval, OAuth, real publish probes, comments, DMs, and recorded evidence."
---

# Social provider qualification

Use this skill when taking one Content Rabbit social provider to production.

Do one provider at a time. Do not claim production readiness from secrets or unit tests alone.

## Capability matrix

Record every operation separately. Use `VERIFIED`, `UNSUPPORTED_BY_PROVIDER`, `NOT_IMPLEMENTED`, or `BLOCKED`.

- Posts: create, read status, update, delete, schedule, and publish each supported media shape.
- Comments: list, read thread, reply, like or react, hide or moderate, mark read, and delete.
- Messages: list conversations, read messages, send, reply, attach media, delete, and use group conversations.
- Authentication: connect, refresh, reconnect, disconnect, and handle revoked scopes.
- Sync: paginate, deduplicate, retry, respect rate limits, and run through the production schedule.

Test only operations that the provider exposes. Link official documentation for every `UNSUPPORTED_BY_PROVIDER` result. Treat `NOT_IMPLEMENTED` as a release blocker when the product promises that operation.

## Evidence gates

Record each gate in the provider report.

Gates 1-4 apply to providers that require a developer app. For a provider that uses its own account-authentication model instead (see Scope boundaries), confirm the dedicated test account and its credentials in place of an app, approval state, callback URL, and secret names.

1. Confirm the provider app exists in its developer console.
2. Confirm its approval state and every approved scope.
3. Confirm the production callback URL matches the deployed service.
4. Confirm the required production secret names exist. Do not copy secret values.
5. Connect a dedicated test account through the real OAuth flow, or through the provider's native account-authentication flow for a provider that uses one instead of OAuth.
6. Publish only neutral test content. Do not name the product or customer unless the operator requests it.
7. Test each supported shape: text, text with one image, multi-image carousel, video, and mixed image plus video when the provider supports it.
8. Verify the public provider page. An API success alone does not prove that media appeared.
9. Test comment sync and reply when the product implements them.
10. Delete each test reply after verification. Record the result. If deletion is unsupported, require an approved retention policy before `READY`.
11. Delete each live test post after its public result and applicable engagement probes are verified. Confirm deletion completed.
12. Test DMs only with a DM adapter and approved scope. Record cleanup or retention for each DM. Require an approved retention policy before `READY`.
13. Record provider-console screenshots, external post URLs, request IDs, failures, and cleanup results.

Never submit an app, publish a test post, reply to a comment, or send a DM without the account owner's approval. Stop when the console requires a password, MFA code, terms acceptance, payment, or final submission confirmation.

## Order

Qualify providers in this order unless the operator chooses another order:

1. X
2. LinkedIn
3. Facebook and Instagram
4. Threads
5. TikTok
6. YouTube
7. Pinterest
8. Bluesky and Mastodon
9. Reddit

Treat Facebook, Instagram, and Threads as separate release gates. Their shared Meta console does not make their scopes or reviews equivalent.

## Local proof

Run the read-only matrix before console work from the `itsryanarmani/scripts` repo root:

```bash
./scripts/social-provider-qualification/qualification-matrix.sh x
```

Set `CONTENT_RABBIT_REPO` to the Content Rabbit checkout path. Replace `x` with the provider slug. The script checks named production secrets and focused handler tests. It does not contact a social provider or create content. This skill depends on `itsryanarmani/scripts#142`. Report `BLOCKED` when the script is unavailable.

For browser work, capture a screenshot before and after each irreversible console action. Keep credentials, tokens, and callback state out of screenshots and notes.

Use a neutral marker such as `integration check <timestamp>`. Never use the product name by default.

After all applicable probes for each live post, confirm deletion from the public provider page. Stop if deletion fails.

## X qualification notes

- Treat a four-image post as X's carousel test.
- Do not test mixed image and video posts. X accepts either images or one video.
- Wait for Cloudflare Stream to report `ready` before publishing a video.
- Confirm the public X post contains the expected image or video element.
- Do not infer OAuth health from an existing connection. Test a new connection separately.
- Record Cloudflare Worker exchange failures as an OAuth blocker when the same exchange succeeds outside Workers.
- X recent search consumes API credits. Disable recurring sync after a bounded test.
- Treat a credit-depleted response as a provider billing blocker. Do not retry it repeatedly.
- Sanitize provider error bodies before returning them through public endpoints.
- X DMs are not implemented in Content Rabbit. Record this as `NOT_IMPLEMENTED` until the adapter ships.

## Scope boundaries

- Comments are implemented for X, LinkedIn, Facebook, Instagram, Threads, and Bluesky. Verify each one separately.
- DMs are implemented only for Facebook and Instagram. Do not promise DMs for other social providers.
- Use native authentication only after official documentation confirms that model. A missing operator secret is not evidence. Otherwise require app authentication or mark `BLOCKED`.
- Do not create an unnecessary developer app for Bluesky.

## Outcome

Mark a provider `READY` only when each applicable operation is `VERIFIED` or documented as `UNSUPPORTED_BY_PROVIDER`. Local proof and every applicable production gate must pass.

Any `BLOCKED` operation blocks the provider. Any promised `NOT_IMPLEMENTED` operation also blocks it. State the exact internal or external blocker.
