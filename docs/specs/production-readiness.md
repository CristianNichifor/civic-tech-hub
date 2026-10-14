# Production readiness

Status: `todo`, `done`, `blocked`, `needs-human`.

| ID | Item | Status |
| --- | --- | --- |
| CTH-1 | Replace the directory with a redirect to the projects hub | done |
| CTH-2 | Archive the GitHub repository | needs-human (owner only) |

## CTH-1 Redirect to the projects hub

Per `digital-public-administration-lab/docs/domain-rollout.md` ("one hub"), the directory
is folded into `https://projects.cristian-nichifor.com/`.

- Given a visitor opens the page,
  when it loads,
  then `<meta http-equiv="refresh">` sends them to `https://projects.cristian-nichifor.com/`.
- Given a crawler reads the page,
  then it finds `<link rel="canonical" href="https://projects.cristian-nichifor.com/">`
  and `<meta name="robots" content="noindex">`.
- Given the refresh does not run,
  then a visible link to the hub is on the page, at 390 px and 1280 px without horizontal overflow.
- Given the README,
  then it starts with "**Archived.**" and points to the hub, mirroring `tablou`.
- Tests: `scripts/check-page.py` (static: refresh, canonical, noindex, link target agree)
  and `tests/page.spec.cjs` (browser: navigation to the hub, fallback link, robots, canonical).
