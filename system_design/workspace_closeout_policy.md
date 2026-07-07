# Workspace Closeout Policy

## Problem

The original v1 harness described task closeout mainly around SC-NMT and other research projects. Session `019ef32c-2559-7a43-848f-f4a87ff12856` showed a gap: a valuable SolidWorks/API modeling task under `G:\projects\燃烧器3d建模绘制` produced reusable assets and verification logs, but was not written to `G:\knowledge` or the harness registries in time.

## Policy

All meaningful work under `G:\` must run workspace closeout before final response. The closeout is mandatory as a check, but capture is selective:

- Capture reusable knowledge only when it is reusable beyond the immediate task.
- Capture reusable prompts only when the prompt can drive future tasks.
- Capture research/project assets when raw materials, reports, figures, CAD outputs, logs, or reproduction entries are useful later.
- Capture decisions when a route, assumption, standard, or system design changes.
- If no capture is needed, explicitly report `closeout checked: no reusable assets`.

## Storage Rules

- `G:\BaiduSyncdisk\ResearchLoop` stores rules, skills, templates, reports, registries, and decision records.
- `G:\knowledge\reusable_knowledge` stores distilled reusable conclusions and workflows.
- `G:\knowledge\reusable_prompts` stores reusable prompt cards.
- Project-local `research_assets` directories store manifests and reproduction entries for project outputs.
- Large raw data, binary CAD files, model weights, temporary files, and uncurated generated files remain in their project or data directories.

## Failure Mode Fixed

Do not stop at “suggested next writeback package.” If the task has already produced a reusable asset and writing a small manifest/card is safe, write it immediately and update the registry.

## Validation

- Registry YAML must parse.
- Registry paths must exist.
- New topics should be retrievable by key terms.
- Unsupported scientific or engineering claims must remain `hypothesis` or `pending validation`.
