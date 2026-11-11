# Launch tooling rules

Rules for any script that creates or changes paid-ad objects. Each rule has a
reason and a check. All of them come from a real first test.

| Rule | Why | How to check |
|---|---|---|
| Run as a dry run by default. Require an explicit flag to send. | A typo in a plan file spends money. A dry run shows every payload first. | Run with no flags. Confirm it prints payloads and makes no API call. |
| Create every object PAUSED. Never set ACTIVE from the create script. | A script that activates can spend before a person reads the result. | Read back `status` on the campaign, ad set and ad. All three say `PAUSED`. |
| Refuse a dead landing page. | An ad that sends clicks to a 404 or a staging page burns budget. | Fetch each link before create. Stop unless it answers 200 on the production host. |
| Read every object back before you activate. | A success reply does not prove the saved state. Platforms drop or change fields. | Read `status` and `effective_status`, budget, start and end dates, targeting, link and Page id. Compare each one with the plan. |
| Back off on the per-account rate limit. | Meta answers code `17`, subcode `2446079` when an account makes calls too fast. A tight retry loop makes it worse. | Wait 60, then 120, then 240 seconds. Stop after 3 tries and report. |
| Never run a create command twice by accident. | A second run makes a second campaign that can also go live. | Before create, list objects with the same name. Stop if one exists. Delete only ids this run created. |
| Run scripts with `python3 -I`. | A local file named like a standard module, such as `math.py`, shadows that module. Imports then load the wrong code. | Run `python3 -I script.py`. Isolated mode ignores the script folder and `PYTHON*` variables. |

## Rollback

- Log each id the moment the platform returns it.
- If a later step fails, delete or pause only the ids in that log.
- Never delete by name match. A name can match an older live object.

## What a run prints

- The plan file name and a hash of its contents.
- Each payload in dry run, with tokens masked.
- Each created id with its read-back status.
- A final line: `paused, ready for review` or the first failure.
