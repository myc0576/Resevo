# 20260627 SC-NMT sequence harness registry

```yaml
id: 20260627_sc_nmt_sequence_harness_registry
project_id: sc-nmt
date: 2026-06-27
status: validated
changed_route_or_assumption: true
```

## Decision

SC-NMT 的 20260624 多实验组 Mie 时序数据先进入 experiment registry 和 Phase 0 sequence freeze manifest；不再把 `原始数据图.tif` / P-011 single-active-TIFF 作为新数据默认入口。

## Context

新数据包含 P012-P021 多个 Mie 序列，每组约 120 帧。P21 还需要在切分前旋转 180°，并在旋转后的视角 1、2 分别记录 ND3.8 和 ND1.9。旧 active-state 流程绑定单帧 TIFF、固定 SHA256 和 P-011 scatter gate，不能安全表达这批数据。

## Alternatives Considered

- 继续扩展 `sc_nmt.active_state`：拒绝。该模块保留旧单帧证据语义，强行扩展会混淆 P-011 历史门控与新序列证据冻结。
- 直接从旧 Phase 2/3 输出开始：拒绝。当前任务不是最终论文重构，且项目规则禁止把 `_archive` 中旧结果作为当前证据。
- 在脚本中按 P21 写特殊分支：拒绝。旋转和滤光片是实验元数据，应由 YAML 和 run manifest 冻结。

## Evidence

- 指标：`python -m pytest tests/test_sequence_dataset.py tests/test_calibration.py tests/test_projection_artifacts.py tests/test_phase2_scatter_masks.py -q`，34 passed。
- 编译：`python -m compileall -q sc_nmt scripts tests`，通过。
- 项目决策记录：`G:\projects\SC-NMT\docs\decision_records\DR_20260624_sequence_harness.md`。
- 架构审计：`G:\projects\SC-NMT\docs\architecture_coupling_audit.md`。

## Impact

- 对 research goal 的影响：新序列可先冻结可追溯输入证据，再决定是否进入去散射、反畸变或重构。
- 对 project route 的影响：新数据入口从 single-active-TIFF 转向 experiment registry + per-run manifest。
- 对 assumption 的影响：P-011 和 `原始数据图.tif` 只保留为历史基线，不再是唯一当前数据源。
- 对 system design 的影响：路径、旋转、视角布局、滤光片和帧数进入配置和 manifest，算法层不写死绝对路径。

## Follow-up

- 后续 Phase 1.6/Phase 2 迁移时，入口应读取 experiment registry 和 Phase 0 manifest。
- P011 LIF 和 P022 pending 不进入当前 Mie 主流程，除非后续有明确任务和人工确认范围。
