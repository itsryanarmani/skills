# Review the exact Apple release candidate

Sources checked November 6, 2026. Recheck them before release.
Use [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) as the policy source.
Use [complete review information](https://developer.apple.com/help/app-review/before-submitting-for-review/complete-review/) for reviewer access and submission details.

Supply source, archive metadata, store drafts and real test artifacts.
Do not supply a desired approval verdict.
Return status, evidence, applicable rule and next action for each check.
Mark unexecuted scenarios UNKNOWN.
Never claim that this simulation guarantees Apple approval.

## Functionality and fleet expansion

Evaluate the current user job, completeness and lasting utility.
Compare related apps for equivalent behavior under rules 4.2 and 4.3.
Distinguish native implementation from useful native behavior.
No arbitrary listing-count threshold establishes approval.
A roadmap does not cure an incomplete release.
Suggest one combined catalog when separate apps repeat the same experience.

## Privacy, support and rights

Trace local storage, off-device transmission, SDKs and external browser actions separately.
Use [Apple's collection definition](https://developer.apple.com/app-store/app-privacy-details/) for privacy labels.
Local storage alone does not establish developer collection.
Check policy access, contact access, deletion statements and public URLs.
Do not invent a clear-all control or promise backup deletion.
Require supporting rights for third-party text and media.

## Device experience and security

Inspect real VoiceOver, larger text, dark appearance, rotation and resizing evidence.
Check custom and standard controls by observed behavior.
Check allowed URL schemes, dependencies, permissions and sensitive outputs.
Do not request capabilities the app does not use.
Do not infer inner-display test coverage from outer-display evidence.

## Build, metadata and assets

Compare archive SDK, minimum OS and device families separately with current requirements.
Trace each screenshot to a real capture from the tested app.
Check required slots, dimensions, opacity and feature claims.
Review all localizations against the selected binary.
Check age questions, category, contact details and review notes.

## Distribution and authority

Require evidence for regions, trader declarations, agreements and encryption answers.
Separate internal-only builds from public candidate eligibility.
List every missing fact without inventing legal declarations.
Keep submission and public release on hold until the owner approves the reviewed result.
