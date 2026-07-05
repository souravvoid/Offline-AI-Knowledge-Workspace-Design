# Repository Standards

## Repository Structure

```
khoji/
├── .github/workflows/     # CI: test, build, release
├── src/frontend/          # React UI
├── src/backend/           # Tauri/Rust backend
├── design/                # Design documents (30 files)
├── models/                # AI model storage (gitignored)
├── docs/                  # Documentation
├── examples/              # Example outputs
├── scripts/               # setup.sh, download-models.sh, dev.sh, build.sh
├── tests/fixtures/        # Test PDFs, images, expected outputs
├── assets/                # Logo, icons, screenshots
├── README.md
├── LICENSE                # AGPL-3.0 (core) / MIT (plugin SDK)
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── CHANGELOG.md
└── ROADMAP.md
```

## README

Must include: badge bar (stars, license, build), feature list, quick start, requirements table (OS, RAM, storage, GPU optional), tech stack table, license, contributing link.

## License

- **Core:** AGPL-3.0
- **Plugin SDK:** MIT (encourage community contributions)

## Git Workflow

```
Branch naming: feature/description, fix/description, docs/description
Commit style: Conventional Commits (feat:, fix:, docs:, refactor:, perf:, test:, chore:)
Format: type(scope): description (e.g. feat(flashcard): add SM-2 scheduling)
```

## GitHub Labels

| Label | Color | Purpose |
|-------|-------|---------|
| bug | #d73a4a | Something isn't working |
| enhancement | #a2eeef | New feature or request |
| documentation | #0075ca | Documentation improvements |
| good first issue | #7057ff | Good for newcomers |
| help wanted | #008672 | Extra attention needed |
| priority: high | #b60205 | Must fix ASAP |
| priority: medium | #fbca04 | Important but not blocking |
| priority: low | #0e8a16 | Nice to have |

## Pre-Commit Hooks

- trailing-whitespace, end-of-file-fixer, check-yaml, check-added-large-files
- `cargo clippy -- -D warnings` on `.rs` files
- `npm run lint` on `.ts/.tsx` files
- `npm run format` on all files
