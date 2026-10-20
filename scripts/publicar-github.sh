#!/usr/bin/env bash
# One-time publication from a trusted developer machine with git and gh authenticated.
set -euo pipefail
OWNER="cortega26"
REPO="nohemi-palencia"
command -v gh >/dev/null || { echo 'Install GitHub CLI (gh) first.' >&2; exit 1; }
command -v git >/dev/null || { echo 'Install git first.' >&2; exit 1; }
ACTUAL="$(gh api user --jq .login)"
[ "$ACTUAL" = "$OWNER" ] || { echo "Authenticated as $ACTUAL, expected $OWNER" >&2; exit 1; }
cd "$(dirname "$0")/.."
python3 scripts/build.py --check
python3 -m unittest discover -s tests -q
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then git init -b main; fi
git add README.md .gitignore index.html templates scripts data tests assets .github
if ! git diff --cached --quiet; then git commit -m 'feat: portfolio artístico de Nohemi Palencia'; fi
if gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
    if ! git remote get-url origin >/dev/null 2>&1; then git remote add origin "https://github.com/$OWNER/$REPO.git"; fi
    git push -u origin HEAD:main
else
    gh repo create "$OWNER/$REPO" --public --description 'Portafolio artístico de Nohemi Palencia Cisneros' --source=. --remote=origin --push
fi
echo "Repository: https://github.com/$OWNER/$REPO"
echo 'Enable GitHub Pages in Settings > Pages when ready to publish.'
