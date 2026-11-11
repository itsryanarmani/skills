# Meta Marketing API traps

Seen on Marketing API v23 during a first test in November 2026. Error codes may change between
versions. Record the version you test against.

| Trap | Why it happens | How to check or fix |
|---|---|---|
| Campaign create fails with subcode `4834011`. | The budget sits on the ad set, and the campaign does not say if ad sets share it. | Set `is_adset_budget_sharing_enabled` on the campaign. Use `false` for one ad set per cap. |
| Ad create fails with subcode `1772103`. | Instagram placements need an Instagram identity linked to the Page. | Link one, or run a first test on Facebook placements only. |
| A housing or real-estate offer runs without a special ad category. | Housing, rental, mortgage and similar offers must declare `HOUSING`, with a country. | Set the category and its country. Expect age 18 to 65+ and no narrow targeting. Plan the audience for that. |
| The budget reads "20" but the account bills in another currency. | An ad account bills in its own currency. Amounts are in that currency's minor unit. | Read the account `currency` before you write a number in a plan or a message. |
| A lifetime budget is refused. | A lifetime budget needs an end date. | Set a placeholder `end_time` at paused create. Reset the real flight at go-live, as `SKILL.md` step 8 says. |
| The marketing token cannot read the Page. | Token scopes differ. A token can fail to read a Page and still use it in a creative. | Do not test by reading the Page. Create the creative with `execution_options=["validate_only"]`. A clean reply proves the Page works. |
| Page create says "too many attempts". | Meta allows only a few new Pages in a short time. The reply is HTTP 200 GraphQL with the error inside. The UI shows nothing. | Stop. Do not retry in a loop. Do not work around it with another account. Try again on a later day. |

## Notes

- A success reply is not proof. Read the object back. See
  [launch-tooling.md](launch-tooling.md).
- Mask tokens in every log line and error message.
- Keep the account, Page and pixel ids in the environment, not in the plan.
