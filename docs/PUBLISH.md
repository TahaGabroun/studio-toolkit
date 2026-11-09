# Maintainer publication

Inspect gh auth status, query both destination repositories, inspect remote contents before changing an existing repository, run tests, inspect git diff/status and scan the staged public file set. Exclude dependencies, caches, credentials, private recordings, personal paths and local skill links. Preserve upstream notices and fonts' own license. Use meaningful commits and main, with no force push.

```bash
gh repo create studio-toolkit --public --source=. --remote=origin --push
```

Run the corresponding command from the demos checkout for studio-toolkit-demos. If a repository already exists, fetch and integrate safely; never replace unrelated history. Verify remote HEAD against the local commit after pushing, and inspect GitHub Actions results. Creating a publication package does not upload a video to YouTube.
