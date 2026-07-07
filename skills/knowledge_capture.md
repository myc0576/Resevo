# Knowledge Capture

用途：把科研任务中产生的可复用知识写成知识卡，而不是聊天摘要。

## Trigger

当任务产生以下内容之一时使用：

- 可复用结论。
- 可复用步骤。
- 关键参数范围。
- 风险边界。
- 验证方法。
- 适用于后续项目的 workflow。

## Procedure

1. 判断类别：`system_engineering`、`3d_reconstruction`、`mie_scattering`、`image_processing`、`scientific_visualization`、`paper_writing`、`experimental_system`。
2. 复制 `templates\knowledge_card_template.md`。
3. 写入 `G:\knowledge\reusable_knowledge\<category>\YYYYMMDD_short_name.md`。
4. 根据证据设置状态：`validated`、`hypothesis` 或 `pending validation`。
5. 更新 `registry\knowledge.yaml`。

## Boundary

不要复制原始实验大数据。不要把临时判断写成确定结论。
