# Branching strategy

Use focused branches to reduce release risk:

- `feat/ios-*`: iOS UI, state management, networking, rendering.
- `feat/backend-*`: backend API, auth, storage, observability.
- `compliance/*`: privacy, moderation, policy controls, audit.
- `exp/*`: prompt/content experiments behind flags.

## Rules

1. Keep one objective per branch.
2. Merge through PR with test evidence.
3. Never combine compliance + feature experiments in the same PR.
4. Tag risky PRs with rollback notes.
