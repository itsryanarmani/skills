---
name: apple-app-release
description: Prepare a native Apple app for tested internal TestFlight distribution and owner-reviewed App Store submission. Use for release evidence, screenshot assets, review checklists, metadata and repeatable updates. Does not replace platform implementation skills.
---

# Release an Apple app with evidence

Prove one useful pilot before expanding to other sites or device families.
Keep internal testing, public submission and public release as separate actions.
Follow the user's existing authorization for each action.
Never promise App Review approval.

## Choose tools and platforms

Use the existing project and build tools first.
Do not install every overlapping MCP server or framework.
Use Apple's Xcode tools where available and a supported build/test interface.
Install upstream skills separately; they are not bundled in this repository.
Use [mobilebuildmcp-cli](https://www.mobilebuildmcp.com/docs/skills) for its supported workflows.
Use [swiftui-expert-skill](https://github.com/AvdLee/SwiftUI-Agent-Skill) for implementation guidance.
Use [swiftui-pro](https://github.com/twostraws/SwiftUI-Agent-Skill) for engineering review.

Apple publishes apps for iPhone, iPad, Mac, Apple Watch, Apple TV and Apple Vision Pro.
An iPhone model is not a separate store platform.
Choose each target for a useful device experience; do not generate empty companions.
Review resizing and input behavior for every supported device configuration.

Read [the policy review prompts](references/review-prompts.md) before choosing fleet expansion.
Similar apps can trigger spam rules even when the developer owns their content.
Consider one catalog app when separate binaries repeat the same user job.

## Establish release inputs

Record the source commit, bundle ID, version, build number and chosen platforms.
List the exact features and data included in this candidate.
Record supported OS versions separately from the build SDK.
Read archive metadata to prove both settings.
Check [current submission requirements](https://developer.apple.com/news/upcoming-requirements/) on each release.
Do not lower the deployment target to satisfy an SDK requirement.

Confirm membership in the developer account; local identities do not prove membership.
Check account role, agreement state and signing access separately.
Apple supports [cloud-managed certificates](https://developer.apple.com/help/account/certificates/cloud-managed-certificates/) without a local distribution identity.
A development-signed archive does not prove distribution export readiness.
Let the Account Holder review legal agreements.
Never publish private signing files, identity details or account evidence.

## Test observable behavior

Write failing user scenarios before implementing a fix.
Prefer the project's E2E runner to tests that repeat implementation details.
Use the environment's required device interface for manual interaction.
Keep project test runners separate from manual device control.
If the device interface fails, follow its recovery advice before choosing an allowed alternative.

Cover first launch, browse, search, detail, saves, relaunch persistence and empty results.
Test offline behavior and each external action the app exposes.
Check physical-device behavior through TestFlight before public release.
Test VoiceOver, larger text, dark appearance, contrast, rotation and resizing.
Standard SwiftUI controls can provide accessibility semantics automatically.
Missing explicit label modifiers do not prove inaccessible controls.
Verify the actual experience before adding redundant labels.

Save result bundles and a small JSON summary outside Git.
Include source commit, destination, OS, command result, duration and artifact paths.
Preserve failed runs and their measured causes.
A later pass alone does not establish why an earlier run failed.
Keep simulator runtime and device compatibility explicit.
A newer runtime might support fewer device types than another installed runtime.

## Prepare truthful assets

Use [app-screenshots](../app-screenshots/SKILL.md) for framing and composition.
Capture actual app UI from the candidate under test.
Keep raw captures and record each finished asset's source capture.
Check [Apple's required screenshot sizes](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/).
Verify format, dimensions, opacity and required device slots.
Generate promotional art only when useful; never present invented art as working UI.
Do not invent an arbitrary minimum UI coverage percentage.

Prepare description, subtitle, keywords, review notes and version changes from shipped behavior.
Mark bundled snapshots and external network requirements accurately.
Do not imply live data, booking, account sync or other features absent from the binary.
Open an asset gallery in the user's chosen browser for review.
Preserve the gallery and individual export files for later inspection.

## Audit before distribution

Run [the review prompts](references/review-prompts.md) against the exact candidate.
Use PASS, FAIL, UNKNOWN or NOT_APPLICABLE for each check.
Attach evidence and an action to every result.
Keep mandatory rules separate from design recommendations.
Keep legal status and content rights unknown until supporting facts exist.
A source file's presence does not prove redistribution rights.

Check privacy/contact access, public URLs, privacy answers, age questions and category.
Check selected regions, trader declarations and export compliance.
Do not infer trader status from free pricing or regional content.
See [Apple's trader guidance](https://developer.apple.com/help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-trader-requirements/).
Use the owner's confirmed legal facts for declarations.

## Deliver internal testing

Reuse existing authorized signing assets and app records.
Avoid duplicate keys, certificates, groups and build uploads.
Export with the intended distribution method after tests pass.
Upload only when internal testing is authorized.
Prefer an internal-only build when public distribution remains on hold.
Such a build cannot later become the public candidate.
Use a new build number for a later public candidate.

Verify processing, compliance status, tester membership and Ready to Test status separately.
Provide concrete test notes and the invitation route.
An accepted upload is not proof that a tester can install the app.
Do not treat internal availability as public App Review approval.

## Make updates repeatable

Reuse existing Mac capacity when cost limits prohibit new paid CI.
Select relevant app, data and brand paths before starting a build.
Do not widen web deployment selection because native files change.
Hash the selected inputs and skip unchanged candidates.
Allocate increasing build numbers and prevent concurrent release runs.
Record the last successful upload only after Apple confirms success.
Preserve failure artifacts and resume without duplicate uploads.
Keep public submission behind the user's explicit review approval.
Do not claim update automation exists until its full path is exercised.

Record setup time separately from build, tests, export, upload and processing time.
Record model usage only for the exact session or job measured.
Separate cached input, output and provider-reported billing.
Do not invent dollar costs from subscription seats or unknown model prices.
Do not claim cost savings without comparable before/after measurements.

## Finish

Use repository issues, local gates, proof and independent review before merge.
Report the tested commit, TestFlight state, open blockers and review asset location.
Pause a progress watcher when no independent work remains.
Submit or release publicly only after the user's explicit review approval.
