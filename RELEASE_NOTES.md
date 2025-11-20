# Release notes — v0.1.0

Release: v0.1.0 (2025-11-20)

Summary
-------
Initial release for the Construction Price Tracker synthetic data utility.

Highlights
----------
- Refactored `generate_data.py` into a CLI-friendly module with type hints.
- Added deterministic synthetic dataset generation and a 7-day moving average.
- Added unit tests (`pytest`) and a CI workflow to run tests on push/PR.
- Added `requirements.txt`, `.gitignore`, `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, and `CODE_OF_CONDUCT.md`.
- Added MIT `LICENSE` and created an annotated tag `v0.1.0`.

How to publish this release (Web)
-------------------------------
1. Open: https://github.com/Pranit-satnurkar/Construction-Price-Tracker/releases/new?tag=v0.1.0
2. Title: `v0.1.0`
3. Release target (tag): `v0.1.0` (already pushed)
4. Fill the release notes with the content from this file or the `CHANGELOG.md` entry.
5. Choose "Publish release".

How to publish this release (CLI with `gh`)
-------------------------------------------
Install and authenticate the GitHub CLI if you haven't already:

```pwsh
# install: https://cli.github.com/
gh auth login
```

Create & publish the release:

```pwsh
gh release create v0.1.0 --title "v0.1.0" --notes-file RELEASE_NOTES.md
```

How to publish this release (curl + PAT)
----------------------------------------
If you prefer the API + Personal Access Token (PAT), run:

```pwsh
$env:GITHUB_TOKEN = '<YOUR_PAT_WITH_repo_scope>'
$body = @{ tag_name = 'v0.1.0'; name = 'v0.1.0'; body = (Get-Content -Raw RELEASE_NOTES.md) }
Invoke-RestMethod -Method Post -Uri 'https://api.github.com/repos/Pranit-satnurkar/Construction-Price-Tracker/releases' -Headers @{ Authorization = "token $env:GITHUB_TOKEN" } -Body ($body | ConvertTo-Json)
```

Notes & Security
----------------
- The PAT needs `repo` scope to create releases for a private or public repository.
- Avoid pasting tokens into chat; prefer running the command locally or setting `GITHUB_TOKEN` in your environment.
