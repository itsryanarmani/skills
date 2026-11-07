# Brand context

## Identity

`itsryanarmani/skills` is a public library of Markdown playbooks for coding agents.
It covers AI-aware software work and personal operations.

The repository is not an application, package, or hosted service. Each skill
teaches one job through instructions, checks, boundaries, and stopping points.

Use this approved descriptor:

> Claude Code skills for AI-aware development and life organization.

The `brand/` directory is a catalog of optional personal-brand directions. It
does not define this repository's visual identity.

## Audience

The primary audience is one solo developer who uses agents as the main
workforce. That reader pays the token, CI, infrastructure, and review costs.

The secondary audience is anyone who installs or copies an individual skill.
Write for that reader without weakening the primary operator's workflow.

Assume technical fluency. Explain vendor traps and safety boundaries without
teaching common shell, Git, or Markdown concepts from first principles.

## Promise

A skill should help an agent complete one named job safely and end to end. It
must stop where human authority, private judgment, or irreversible action begins.

The library turns live operating knowledge into reusable instructions. A
verified run outranks stale prose, and a correction belongs in the skill.

Shared contracts prevent related skills from inventing competing workflows.
Use an existing router or domain contract before adding another entry point.

## Message hierarchy

Lead with these ideas, in order:

1. Name the job the skill completes.
2. State the decision or safest next action.
3. Show the exact workflow and verification.
4. Name failure modes, limits, and human gates.
5. Link related skills only when they own the next step.

Do not market the repository as a general AI framework. It is an operating
library of task-specific playbooks.

## Voice

Write in a direct, evidence-led, operator voice.

- Lead with the answer or action.
- Use active verbs and concrete nouns.
- Explain why when it changes a decision.
- Prefer measured facts over broad praise.
- Name costs, failure modes, and unsupported paths.
- State safety limits as commands, not suggestions.
- Mark unknowns instead of filling them with plausible detail.
- Keep humor rare and subordinate to the task.

Avoid promotional filler such as "seamless," "powerful," "revolutionary," or
"best-in-class." Avoid claims that a command is safe without naming its guard.

## Naming

- Write the repository name as `itsryanarmani/skills`.
- Write skill names in lowercase kebab-case.
- Keep a skill directory and its frontmatter `name` identical.
- Use the established family prefix when a family exists.
- Keep a standalone name when no family exists.
- Write the instruction file as `SKILL.md`.
- Use product and vendor capitalization from their official documentation.

The prefix describes the skill family, not the vendor. Do not create a family
of one for visual neatness.

## Claims and evidence

Ground factual claims in repository evidence or a primary external source.

- Prefer a live, recorded run over vendor documentation.
- Prefer official vendor documentation over summaries.
- Date facts that can change.
- Attach before-and-after measurements to cost or performance claims.
- Distinguish a tested fact from a proposed workflow.
- Never store personal data, credentials, or private payloads as evidence.

Do not repeat time-sensitive repository counts in durable copy. The catalog
changes often, and nearby documents already show how quickly counts drift.

## Marks and assets

The repository has no canonical logo, icon, color palette, or typeface. Use the
plain text name `itsryanarmani/skills` as its wordmark when a label is required.

Do not adopt a direction from `brand/` as the repository mark. Do not invent an
agent mascot, gradient, monogram, or vendor-style logo without a separate brand
decision and supporting assets.

## Anti-patterns

- Do not describe planned behavior as shipped behavior.
- Do not turn one skill into a broad framework.
- Do not create a second router for an existing domain.
- Do not duplicate a shared contract inside every related skill.
- Do not soften explicit approval or submission gates.
- Do not hide a known failure mode behind general advice.
- Do not use private user data in examples.
- Do not present the `brand/` catalog as this repository's chosen style.
