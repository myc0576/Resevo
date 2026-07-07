# Decision: Rename Public Project Branding To ResearchLoop

## Status

validated

## Context

The project previously used `Research Harness` and `research-harness` as public-facing names. That wording was easy to confuse with the local directory path and with the generic workflow concept of a harness.

## Decision

Use **ResearchLoop** as the public project brand.

Canonical positioning:

`ResearchLoop: a self-evolving workflow harness for paper-driven research and reusable knowledge assets.`

The canonical local entry is now `G:\BaiduSyncdisk\ResearchLoop`. Historical ids, file names, or schema markers may still use `research_harness` when changing them would create a migration unrelated to public branding.

## Consequences

- Public-facing documentation should say ResearchLoop.
- Local path references should use `G:\BaiduSyncdisk\ResearchLoop`.
- Historical ids, schema names, file names, and compatibility markers may keep `research_harness` when changing them would create a migration unrelated to branding.
- Publication preparation should keep raw data, images, model weights, generated state, run traces, secrets, and local-only outputs out of commits.

## Verification

- README and Chinese README carry the new brand, homepage narrative, and local-path note.
- `harness.yaml` exposes the brand metadata.
- `.gitignore` blocks local generated state, traces, raw data, images, model weights, secrets, and large research assets by default.
