# Decision Record: Nature Skills Starter Workflow Onboarding

```yaml
id: 20260708_nature_skills_starter_workflow_onboarding
project_id: researchloop
date: 2026-07-08
status: pending validation
allowed_status:
  - validated
  - hypothesis
  - pending validation
changed_route_or_assumption: true
```

## Decision

ResearchLoop will offer `Yuan1z0825/nature-skills` as an optional first-use
starter workflow. The repository owns the onboarding prompt, installer script,
registry entry, documentation, and validation tests. The upstream repository
stays outside committed source under the ignored local path
`external\nature-skills`.

## Context

ResearchLoop already avoids embedding LLMs, raw research data, large generated
outputs, and external conversion repositories. The user wants future ResearchLoop
users to start from a useful research workflow seed while retaining the ability
to adapt or replace it for their own scientific work.

## Rationale

- A consent-first installer gives new users a clear starter path without
  silently downloading third-party code.
- Keeping the full upstream checkout under `external\nature-skills` preserves
  upstream structure, license context, and future update paths without vendoring
  the source into ResearchLoop.
- A project-level upstream workflow registry lets future open-source workflow
  integrations reuse the same metadata and validation pattern.
- Clone-and-reference avoids changing `%USERPROFILE%\.codex\skills`, installing
  dependencies, configuring credentials, or mutating user-level agent state.

## Consequences

- First-use agent instructions must run installer `status` and ask before
  running `install`.
- `external/` remains ignored, so downloaded upstream source is local-only.
- `registry/upstream_workflows.yaml` becomes the machine-visible index for
  optional starter integrations.
- Nature Skills usage remains `pending validation` until a real local workflow
  run produces ResearchLoop closeout evidence.

## Verification

- `python -m py_compile scripts\starter_workflow_installer.py scripts\registry_tool.py scripts\evaluator.py scripts\_harness_common.py`
- `python -m pytest`
- `python scripts\starter_workflow_installer.py status --id nature-skills --json`
- `python scripts\registry_tool.py validate`
- `python scripts\evaluator.py evaluate --target all --json`
- `python scripts\kb_index.py rebuild`
- `python scripts\closeout_check.py`
