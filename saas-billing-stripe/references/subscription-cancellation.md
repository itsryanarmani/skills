# Subscription cancellation flow

Ship cancellation with every paid product. Apply this contract to each site
in a multi-site product. Use the site's existing billing service and design system.

Use the reference flow's structure. Write the questions and value messages
for the current product. Never copy another product's prices or success claims.

## Before implementation

1. Find the current billing settings, cancellation handler, and webhook handler.
2. Record the actual trial, renewal, access, export, retention, and deletion rules.
3. Find the site's settings service, admin API, CLI, and MCP tools.
4. Define failure cases as E2E assertions before writing application code.
5. Reuse the current billing path and permission checks.

Cancellation ends a subscription. Account deletion is a separate action.
Explain when access ends and what data remains. Do not invent permanent loss,
customer loss, credit forfeiture, or automatic deletion to encourage retention.

## Screens and branches

Use one responsive dialog or page with consistent Back and Close controls.
Keep cancellation visible in billing settings. Never hide it behind “Show more.”
Allow direct continuation to confirmation from every retention screen.

| Screen | Content and action | Next state |
| --- | --- | --- |
| Modify subscription | Show the current plan and actual price. Show upgrade, trial extension, downgrade, and cancel actions when supported. | The chosen action or reason selection. |
| Expanded options | Explain unavailable actions with actual eligibility details. Keep cancel visible in both layouts. | The chosen action. |
| Reason selection | Show site-specific reasons with short descriptions. Include Other and Skip. Show the actual trial or renewal date. | One matching offer, or impact review. |
| Setup or results help | Offer a working guide, checklist, or support route for this product's task. | Accept help, or continue cancellation. |
| Feature problem | Ask which product feature fails and what the user expects. Feedback remains optional. | Relevant help, or impact review. |
| Price offer | Show an eligible discount with its duration, currency, invoice amounts, and later price. | Explicit acceptance, or impact review. |
| Specialist help | Show the actual support service and a valid contact or booking route. | Open support, or impact review. |
| Value guide | Show a short plan for the product's outcome. Include measured results only when evidence exists. | Open the guide, or impact review. |
| Impact review | Show the paid features and verified account values affected by cancellation. State when each change takes effect. | Confirm, optional pause, or return. |
| Pause offer | Show preserved data, disabled features, duration, restart date, and all charges. Show this only when billing supports it. | Explicit acceptance, or confirmation. |
| Feedback | Ask an optional follow-up based on the selected reason. Use neutral prompts and a Skip action. | Confirmation, or an eligible offer. |
| Final offer | Show at most one eligible alternative after feedback. Do not restart the offer sequence after refusal. | Explicit acceptance, or confirmation. |
| Confirmation | Summarize the subscription, effective date, final charge, access, and data policy. Provide a clear Cancel subscription action. | A pending result, success, or a retryable error. |
| Completion | Show the confirmed cancellation date and remaining access. Show reactivation or support only when supported. | Return to billing or the account. |

Feedback and offers must never become required steps. Use neutral decline labels,
such as “Continue cancellation.” Avoid guilt messages such as “I don't need customers.”

Closing the flow changes nothing unless the user already confirms a billing action.
Preserve progress during errors. Do not repeat an accepted or declined offer on Back.
Do not require a new password for cancellation unless the existing security policy requires it.
Support the existing passwordless and social sign-in methods when authentication must be repeated.

## Write reasons for the site

The category stays stable for reporting. The displayed wording belongs to the site.
Reason IDs remain stable when an administrator changes their labels.

| Product shape | Example reasons | Example impact values |
| --- | --- | --- |
| Content publishing | Output quality, brand voice, publishing connections, content volume, price. | Scheduled posts, connected channels, saved drafts, paid generation allowance. |
| Page builder | Editing, templates, domain setup, publishing, site performance, price. | Published pages, custom domains, forms, paid hosting features. |
| Listing directory | Listing visibility, lead quality, listing management, paid placement value, price. | Paid placements, listing limits, lead tools, renewal date. |

Treat these as starting points. Inspect the actual product before setting defaults.
Each reason can define a follow-up question and one relevant help or offer branch.
For price feedback, ask what plan or price fits the user's needs.
For feature feedback, use the site's actual feature names.

Read impact values from authorized account data. Include a count or amount only
when the system can verify it. Omit unavailable values rather than estimating them.
Distinguish loss of a paid feature from loss of stored data.
Do not say cancellation causes lost customers or revenue without direct evidence.

## Editable configuration

Store configuration under the existing site identity. A tenant account must not
change the global flow. Separate site administrators from account billing owners.

Expose the same versioned configuration through the admin API, CLI, and MCP tools.
Use one validation and authorization service for all three surfaces.
Reuse existing settings commands and tools when they already support structured values.

| Field group | Editable values |
| --- | --- |
| Identity | Site ID, locale, configuration version, enabled state. |
| Copy | Titles, descriptions, buttons, help links, completion messages. |
| Reasons | Stable ID, category, label, description, order, enabled state, follow-up prompt. |
| Routing | Reason-to-offer mapping, eligible plan IDs, trial rules, maximum offer count. |
| Value messages | Product feature labels, impact descriptions, approved account metric keys. |
| Offers | Enabled state, billing price or coupon reference, duration, limits, help destinations. |
| Pause | Supported plan reference, period, charges, restart behavior, consent text. |

Keep access, retention, export, and deletion policies in their existing policy service.
Render those facts beside the editable copy. Reject copy that contradicts those facts.

Support read, validate, update, and reset through each admin surface.
Return a version on reads. Require the expected version on updates to prevent lost edits.
Validate unique reason IDs, routes, limits, lengths, locales, and allowed metric keys.
Accept only approved HTTPS destinations or existing internal routes.
Resolve billing references on the server. Do not accept arbitrary discounts from a customer.
Audit the actor, site, time, version, and changed fields for each update.
Restrict feedback access and apply the product's retention policy.

Ship defaults for every paid site. Permit site overrides through the settings service.
A change for one site must not change another site's flow.
Check effective configuration across the site registry before release.
Do not require a rebuild to publish validated text, reason, or offer changes.
Use an explicit cache version or invalidate the bounded site settings cache.

## Billing execution

Never apply an offer because the user views a screen, selects a reason,
submits feedback, closes the dialog, or returns to billing.
Say “available” until the billing service confirms acceptance.
Say “applied” only after confirmed success. Do not copy a “pre-applied” badge otherwise.

Authorize the billing owner against the site's subscription on every mutation.
Resolve customer and subscription IDs on the server.
Recheck eligibility and configuration version immediately before an offer action.
Reject expired, repeated, conflicting, or unsupported offers.
Show the current terms again if configuration changes during the flow.

Make repeated confirmation safe with an idempotency key.
Store the confirmed provider result and reconcile it through the existing webhook path.
Do not let late events restore stale access or duplicate a discount.
Handle an already-cancelled or scheduled subscription as a valid existing result.
Show scheduled cancellation separately from immediate cancellation.
Keep access through the paid period when that is the product's billing rule.

A provider timeout is an unknown result. Reconcile before retrying the mutation.
Keep cancellation available if feedback storage, analytics, or an offer service fails.
Do not require all browser steps on the server before allowing an authorized cancellation.

## Evidence before release

Run browser E2E checks against isolated accounts and test billing data.
Run the repository's full required E2E suite on the merge candidate.
Do not add browser E2E to the fast PR gate.
Clean up only the data created by the run.

Verify these cases:

- Cancel from billing, skip feedback and offers, confirm, and observe the provider result.
- Accept each supported alternative and verify its actual billing effect and consent.
- Decline all alternatives without a loop or hidden cancellation action.
- Close or go Back without an unintended billing change.
- Verify trial, active, scheduled, cancelled, and unsupported plan states.
- Repeat confirmation and deliver duplicate or delayed webhooks without duplicate effects.
- Simulate provider failure and timeout without false success or duplicate charges.
- Fail feedback and analytics while cancellation still completes.
- Verify paid access and stored data match the stated effective date and policy.
- Edit each field group through API, CLI, and MCP as a site administrator.
- Read the edited values through the other surfaces and in a fresh browser session.
- Reject unauthorized writes, cross-site reads, invalid references, and stale versions.
- Verify distinct effective reasons and value messages for every paid site.
- Verify keyboard navigation, focus restoration, small screens, and readable error states.

Save before and after screenshots outside the repository.
Attach them to the PR. Save a repeatable JSON report with site IDs, configuration
versions, test outcomes, and confirmed billing states. Exclude credentials and personal feedback.
Include the exact commands and results in the PR.
