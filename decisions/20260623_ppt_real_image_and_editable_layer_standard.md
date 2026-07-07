# Decision Record: PPT Real Image And Editable Layer Standard

```yaml
id: 20260623_ppt_real_image_and_editable_layer_standard
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

SC-NMT 后续科研 PPT 中，方法示意图、公式页和结果页应优先采用图文非耦合结构；能使用真实观测图或真实数据衍生图时，不再默认使用虚拟生成示意图。

## Context

会话 `019ebb27-d005-7061-bba7-16681a670b9c` 中，用户多次要求优化 Phase 2.6 PPT 的真实感、可编辑性和直接写回原文件，并进一步要求将 `观测 y1 / y2 / yk` 替换成真实图像。后续 20260622 组会 PPT 又明确要求从第 9 页起重绘所有科学示意图，避免截图式耦合图片。

## Alternatives Considered

- 保留整页截图或截图式示意图：不采用，因为文字、公式、色标和图像耦合，后续审稿和组会修改成本高。
- 继续使用虚拟生成观测图：不采用，因为用户明确要求替换为真实观测图，且真实图更符合科研证据链。
- 全部改成位图：不采用，因为公式、标注、图题和色标说明需要可编辑。

## Evidence

- Phase 2.6 PPT 最终直接更新原文件，虚拟观测图替换为真实 Mie 图像衍生版本。
- 20260622 组会 PPT 输出图文非耦合重绘版，第 9-11 页和第 21 页无图片对象。
- 会话中多次执行页数、媒体非空、目录清理和预览检查。

## Impact

- 对 research goal 的影响：提高 SC-NMT 可发表图件和组会材料的可维护性。
- 对 project route 的影响：PPT 产出从“截图式快速生成”转向“真实数据图像本体 + 可编辑解释图层”。
- 对 assumption 的影响：不再默认认为生成式虚拟图能替代真实观测图。
- 对 system design 的影响：后续 closeout 应把 PPT 视觉/图层经验写入 scientific visualization knowledge 和 prompt registry。

## Follow-up

- 后续 PPT 任务结束时检查是否产生新的审美规则、Prompt 或素材资产。
- 若用户对新版 PPT 审美进一步确认或修正，应追加新的 knowledge card revision。
