# SC-NMT PPT 科学图像必须使用伪彩

## Decision

自 2026-07-01 起，SC-NMT 所有 phase/report/manuscript PPT 中的科学数据图层必须使用伪彩，不得插入灰度图像。伪彩配色默认沿用 `G:\projects\SC-NMT\calibration\qc` 的 `inferno`。灰度数组只能作为 OpenCV 棋盘格检测、反畸变、阈值分割或其他数值计算的内部输入，不能作为 PPT 输出图层。

## Rationale

灰度图在六视角标定、Mie 强度、残差和体数据切片里容易弱化动态范围差异，也不满足当前用户对 PPT 证据图的审查要求。伪彩输出可以保持诊断可读性，同时让色标范围、图注和视角编号作为可编辑 PPT 对象独立审计。

## Scope

- 适用于 Phase 0-8 所有阶段 PPT、人工复核 PPT、论文图 PPT 和投稿前审计 PPT。
- 适用于检测覆盖图、伪彩质量图、重投影残差图、体数据切片、时序代表图和标定诊断图。
- 不改变原始数据、不改变标定数值、不提升人工 gate。

## Implementation Notes

- 默认伪彩：`inferno`，与 `G:\projects\SC-NMT\calibration\qc` 保持一致。
- PPT audit 必须检查内嵌媒体是否为单通道或 RGB 三通道同值的灰度样式。
- 若发现灰度样式图片，该 PPT 进入 block，必须重新导出伪彩数据图层。
- 标题、视角编号、箭头、色标、比例尺和图注仍必须为 PPT 可编辑对象，不得烧入图像像素。

## Verification

2026-07-01 已在 SC-NMT Phase 2.3 补拍棋盘格标定脚本中加入 PPT 内嵌图片审计，并生成 inferno 伪彩合并优化产物：

```text
G:\projects\SC-NMT\outputs20260628\runs\phase2_20260701_loop1\phase2_3_checkerboard_best_view_gallery_inferno_merged
```

该产物的 `phase2_3_best_view_gallery_pptx_audit.json` 记录：

```text
ppt_data_colormap = inferno
embedded_image_count = 24
grayscale_like_image_count = 0
```
