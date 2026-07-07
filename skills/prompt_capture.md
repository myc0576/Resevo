# Prompt Capture

用途：保存可复用 Prompt，使后续 Codex、Claude、ChatGPT 或科研可视化任务可以复用。

## Trigger

当任务中出现能稳定复用的 prompt、角色提示、审稿提示、图像生成提示或项目复盘提示时使用。

## Procedure

1. 判断类别：`codex`、`claude`、`chatgpt`、`scientific_visualization`、`paper_writing`、`project_review`。
2. 复制 `templates\prompt_card_template.md`。
3. 写入 `G:\knowledge\reusable_prompts\<category>\YYYYMMDD_short_name.md`。
4. 记录 task、input、output、prompt body、model、notes、revision history。
5. 更新 `registry\prompts.yaml`。

## Boundary

不要保存一次性闲聊。不要保存缺少任务、输入和输出边界的 prompt。
