# Decision Record: PPT Bitmap Effective DPI Audit Standard

```yaml
id: 20260623_ppt_bitmap_effective_dpi_audit_standard
project_id: sc-nmt
date: 2026-06-23
status: validated
allowed_status:
  - validated
  - hypothesis
  - pending validation
changed_route_or_assumption: true
```

## Decision

SC-NMT 后续科研 PPT 的图文非耦合审计中，必须增加位图有效分辨率检查：对每一个 PPT 图片对象，按图片像素尺寸和页面中的显示尺寸折算有效 dpi，若 `min(px_width / display_width_in, px_height / display_height_in) < 300`，则判为最终论文级 PPT 的未达标项。

此规则只针对位图科学图像本体；PPT 原生文本、公式、矢量形状、原生图表不按此规则检查。

## Context

用户要求检查 `C:\Users\Administrator\Desktop\20260622组会汇报_图文非耦合重绘版.pptx` 是否采用可复用资产并遵循规则。审计确认该 PPT 已基本满足“可复用资产 + 图文非耦合”要求，但发现部分位图虽然来自项目可复用资产，按当前 PPT 展示尺寸折算后低于 300 dpi。

这说明仅检查“图片是否来自项目资产”和“文字是否可编辑”仍不够；若位图被放大使用，仍可能不满足论文级清晰度要求。

## Alternatives Considered

- 只检查图片源文件是否可追溯：不采用，因为源文件可追溯并不保证展示尺寸下达到 300 dpi。
- 只做肉眼预览检查：不采用，因为预览图难以稳定发现轻度低分辨率问题。
- 一律禁止位图：不采用，因为真实观测图、切片、残差图和体渲染图本身必须作为科学图像本体保留。
- 允许所有低 dpi 图作为组会草稿：只可作为 review-only 状态；若标注为论文级或最终版，应触发修复。

## Evidence

- 审计对象：`C:\Users\Administrator\Desktop\20260622组会汇报_图文非耦合重绘版.pptx`
- 审计结果：
  - 第 9-23 页共有 45 个图片对象。
  - 45/45 图片对象均能通过哈希匹配到 `G:\projects\SC-NMT\outputs\...` 下的可复用项目资产。
  - 第 9-11 页和第 21 页无图片对象，说明公式页和排名图已实现图文非耦合。
  - 页面比例为 16:9，且第 9-23 页对象越界数为 0。
  - 仍有 12 个图片对象按展示尺寸折算低于 300 dpi，主要集中在观测图、残差图、权重曲线和第 20 页三向投影图。
- 可复现检查逻辑：
  - 对每个 PPT 图片对象读取嵌入图片像素尺寸。
  - 读取该图片对象在 PPT 中的显示宽高，单位换算为英寸。
  - 计算 `effective_dpi = min(px_width / display_width_in, px_height / display_height_in)`。
  - 输出 `low_dpi_count` 和具体页码、图片对象名、像素尺寸、显示尺寸、有效 dpi。

## Impact

- 对 research goal 的影响：提高 SC-NMT 组会 PPT 到论文图件之间的可迁移性，避免“图文可编辑但位图不够清楚”的隐性质量缺口。
- 对 project route 的影响：PPT closeout 从单纯的图文分离审计，扩展为“资产可追溯 + 图文非耦合 + 有效 dpi”三项联合审计。
- 对 assumption 的影响：不再默认认为来自项目输出目录的图片一定满足最终 PPT 清晰度要求。
- 对 system design 的影响：后续 scientific visualization 和 PPT 任务结束时，应把低 dpi 图片列为显式待修复项，而不是笼统称为已通过。

## Follow-up

- 后续 PPT 生成或重绘任务的最终检查应报告：
  - `pictures_total`
  - `matched_reusable_assets`
  - `unmatched_assets`
  - `low_dpi_count`
  - `low_dpi_details`
  - `out_of_bounds_count`
- 若 `low_dpi_count > 0`，最终回复不得直接称为“论文级最终版”；应说明“图文非耦合已通过，但位图有效分辨率仍需提高”。
- 修复策略优先级：
  - 从科学数据重新导出更高分辨率图像。
  - 减小位图在 PPT 中的显示尺寸。
  - 能用 PPT 原生图表替代的曲线图，改成原生图表。
  - 若仅用于内部组会预览，应明确标注为 review-only，不标为 final/publication-ready。
