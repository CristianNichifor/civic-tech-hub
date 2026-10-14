# civic-tech-hub

Archived: `index.html` is a redirect page to the projects hub at https://projects.cristian-nichifor.com/. Project links live in the hub (digital-public-administration-lab), not here. Keep the refresh target, canonical link, fallback link and `noindex` in agreement.

## Setup and verification

Node 22 and Python 3.12: `npm ci`, then `npx --no-install playwright install chromium` once. Run `npm run check` for the static redirect checks and `npm test` for the browser redirect and fallback checks. These need no credentials or live upstream projects. There is no production build step; npm installs only development test tools.

Preview with `python3 -m http.server 8000 --bind 127.0.0.1 --directory .`. CI reports `verify`. External site availability is operational evidence, not a deterministic PR correctness gate.

## Contribution workflow

- Work from the remote default branch in a separate checkout. With the maintainer's `wt` tool, run `git fetch origin` then `wt new chore/<task> origin/dev`; it creates `<repo>/.worktrees/chore/<task>`. Contributors without `wt` can use a separate clone and feature branch. Never modify another task's working tree.
- Use Conventional Commits: imperative lower-case subject, at most 72 characters, no trailing full stop, one change per commit. Explain why in the body only when needed; link issues with `Refs: #N` or `Closes: #N`.
- Open a PR against `dev` with the problem, resulting behavior, verification command/results and any limitations. Agents may squash-merge a PR into `dev` once verification passes and every required check is green; they never merge into `main`, promote `dev` to `main`, push directly to protected branches, bypass rules, deploy, or publish releases — promotion and public visibility stay with the owner.
- A required check or administrator-only branch rule is not an agent permission boundary: administrator credentials can bypass rules. Keep publication credentials out of ordinary development.
- Tasks need an observable acceptance criterion, affected area, constraints and a verification command. Use synthetic fixtures; do not include credentials or personal data in issues, logs or tests.
