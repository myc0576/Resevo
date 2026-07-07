# Release Pack

## GitHub README Checklist

- [x] GitHub README would state the fixture scope.
- [x] Minimal reproduction command is visible.
- [x] data/code availability statement is included.
- [x] Paper-to-repo crosslink checklist is represented by output object links.

## LICENSE Checklist

- [x] LICENSE review is not needed for the internal text fixture.
- [x] No third-party data.

## CITATION.cff Checklist

- [x] CITATION.cff is not required for the dry-run.
- [x] Future real release must add CITATION.cff.

## Release Notes Checklist

- [x] release notes: first minimal paper lifecycle fixture.
- [x] known limitation: structure-only.

## Data/Code Availability Statement

The dry-run uses tiny text fixtures committed inside `examples/paper_lifecycle_minimal`; no real experimental data is copied.

## Zenodo/DOI Checklist

- [x] Zenodo DOI is not required for this dry-run.
- [x] Real release must archive code/data package separately.

## Minimal Reproduction Command

```powershell
python scripts\validate_research_project.py --project-root examples\paper_lifecycle_minimal --json
```

## Demo Assets

- demo_figure: `results/figure_v1.txt`
- demo_notebook: none
- demo_video_or_gif: none

## Paper-To-Repo Crosslink Checklist

- [x] output object links to claim C1.
- [x] figure F1 links to claim C1.
- [x] release pack links to reproduction command.

## Release Gate

- release_ready: yes for dry-run.
- blocker: none.
- next_action: run validator.
