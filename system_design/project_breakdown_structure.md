# Project Breakdown Structure

状态：`pending validation`

本文件给出 ResearchLoop 的项目分解结构。它不是任务清单，而是帮助 Codex 判断任务结束后应该沉淀到哪里。

## Layer 1: Project Work

- SC-NMT active research tasks。
- 其他科研项目任务。
- 实验、代码、图像、PPT、论文材料相关工作。

## Layer 2: Closeout Products

- Reusable knowledge card。
- Reusable prompt card。
- Research asset manifest。
- Experiment review。
- Decision record。

## Layer 3: Storage

- Knowledge cards 写入 `G:\knowledge\reusable_knowledge\<category>`。
- Prompt cards 写入 `G:\knowledge\reusable_prompts\<category>`。
- Research assets 写入当前项目 `research_assets\YYYYMMDD_task_name`。
- Registries 写入 `G:\BaiduSyncdisk\ResearchLoop\registry`。

## Layer 4: Validation

- 有指标、残差、相关系数、对比图、运行日志或复现命令时，状态可设为 `validated`。
- 只有推断而无验证证据时，状态必须设为 `hypothesis`。
- 已有明确验证计划但尚未执行时，状态设为 `pending validation`。
