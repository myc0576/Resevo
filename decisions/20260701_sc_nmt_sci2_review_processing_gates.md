# SC-NMT SCI 2 Review Processing Gates

```yaml
id: 20260701_sc_nmt_sci2_review_processing_gates
date: 2026-07-01
project_id: sc-nmt
status: pending validation
changed_route_or_assumption: true
```

## Decision

SC-NMT 后续处理路线增加 SCI 2 区审查反馈门槛：不能从 Phase 2.2 前置证据直接跳到论文图或投稿结论；必须先完成 Phase 2.3 新视场联合标定、Phase 2.4 observation package、Phase 5 baseline、Phase 6 新方法对照和 Phase 7 时间统计。

## Reason

审查意见认为项目有方法创新潜力，但当前证据链尚未闭合。把审查意见写入处理门槛，可以避免后续任务把方法设想、visual hull、单帧截图或支持域误写为已验证三维 Mie 散射强度体。

## Evidence

- Project guidance: `G:\projects\SC-NMT\docs\sci2_review_processing_guidance_20260701.md`
- Project decision record: `G:\projects\SC-NMT\docs\decision_records\DR_20260701_sci2_review_processing_gates.md`
- Project asset manifest: `G:\projects\SC-NMT\research_assets\20260701_sci2_review_feedback\00_asset_manifest.md`

## Boundary

This decision validates route guidance only. It does not validate reconstruction results, does not approve paper readiness, and does not promote `approved=true`, `current_gate=pass`, or `paper_ready=true`.

