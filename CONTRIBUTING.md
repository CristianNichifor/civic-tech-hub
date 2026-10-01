# Contributing

A static bilingual link directory. Projects own their code and release independently. Edit `index.html`; do not introduce a shared application runtime. Add projects with a public source URL, a working destination and a short accurate description. Keep Romanian and English text consistent.

Install Node 22, Python 3.12 and the locked test dependencies with `npm ci`; install Chromium with `npx --no-install playwright install chromium`. Before a PR, run `npm run check` and `npm test`. Include desktop/mobile screenshots for visual changes and explain new project inclusion or changed URLs. No account or production deployment is needed for local verification.

## Contribution workflow

- Work from the remote default branch in a separate checkout. With the maintainer's `wt` tool, run `git fetch origin` then `wt new chore/<task> origin/dev`; it creates `<repo>/.worktrees/chore/<task>`. Contributors without `wt` can use a separate clone and feature branch. Never modify another task's working tree.
- Use Conventional Commits: imperative lower-case subject, at most 72 characters, no trailing full stop, one change per commit. Explain why in the body only when needed; link issues with `Refs: #N` or `Closes: #N`.
- Open a PR against `dev` with the problem, resulting behavior, verification command/results and any limitations. Agents never merge PRs, push directly to protected branches, deploy, or publish releases.
- A required check or administrator-only branch rule is not an agent permission boundary: administrator credentials can bypass rules. Keep publication credentials out of ordinary development.
- Tasks need an observable acceptance criterion, affected area, constraints and a verification command. Use synthetic fixtures; do not include credentials or personal data in issues, logs or tests.
