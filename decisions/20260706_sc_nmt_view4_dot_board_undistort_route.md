# SC-NMT view4 圆点标定板反畸变演示路线

```yaml
id: 20260706_sc_nmt_view4_dot_board_undistort_route
project_id: sc-nmt
date: 2026-07-06
status: pending validation
allowed_status:
  - validated
  - hypothesis
  - pending validation
changed_route_or_assumption: true
```

## Decision

SC-NMT `plan20260627.md` 的 Phase 2 路线从旧的 `20260624scale` 十组标尺预审，调整为 2026-07-06 补拍圆点标定板的 view4-first 标定和反畸变演示路线。圆点板路径为 `G:\data\experiments\2026\20260706（0624）标尺补拍`，圆点直径 1.0 mm，圆点中心距 2.5 mm。本轮只要求 view4 形成可复核标定/反畸变演示；其他视角失败不阻断 view4，但必须记录失败状态。

## Context

用户已经补拍圆点标定板，并希望先用 view4 做标定演示，同时补齐反畸变流程。传像束探头和喷雾器相对位置没有变化，因此计划将固定探头-喷雾器几何作为三维空间预飞行先验，但不把该先验伪装成新的六视角完整标定结果。

## Alternatives Considered

- 继续以 `20260624scale` 十组旧标尺作为 Phase 2 主输入；拒绝原因：当前已有 2026-07-06 圆点板补拍，旧数据应降级为历史参考和失败原因对照。
- 要求六个视角全部标定成功后再进入反畸变；拒绝原因：当前用户明确只要求 view4 标定演示，其他视角失败可接受。
- 直接进入三维重构；拒绝原因：view4 演示和三维空间预飞行尚未产生数值验证、manifest、PPT 和 figure contract。

## Evidence

- 计划文件已更新：`G:\projects\SC-NMT\plan20260627.md`。
- 当前补拍圆点板路径存在：`G:\data\experiments\2026\20260706（0624）标尺补拍`。
- 本记录只保存路线决策；未复制原始实验数据。
- 未运行 view4 圆点检测、相机标定、反畸变或三维重构。

## Impact

- 对 research goal 的影响：优先获得可演示、可审计的 view4 反畸变链路，再推进三维空间预飞行。
- 对 project route 的影响：Phase 2 增加 view4-first 标定、view4-first observation package 和 Phase 2.5 三维空间坐标系/体素网格预飞行。
- 对 assumption 的影响：固定探头-喷雾器相对位置成为显式几何先验，需要后续验证和 provenance。
- 对 system design 的影响：后续需要圆点板检测、空间预飞行、三维轴测图 contract 和对应测试。

## Follow-up

- 先建立补拍圆点板 manifest 和 view4 检测 overlay。
- 再生成 view4 的 Knew、畸变参数、remap、P_undistorted 和反畸变强度审计。
- 最后生成 `world_coordinate_frame.json`、`voxel_grid_candidate.json`、`axonometric_view_config.yaml` 和 figure contract 草案。
