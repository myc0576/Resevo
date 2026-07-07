from __future__ import annotations

from pathlib import Path

from _harness_common import REGISTRY_FILES, append_ledger, now_iso, read_yaml, write_yaml


REPAIRS: dict[Path, str] = {
    Path("G:/knowledge/reusable_knowledge/system_engineering/20260623_historical_session_ingestion_workflow.md"): r"""# SC-NMT 历史 Codex 会话批量沉淀工作流

status: validated
source_project: sc-nmt
updated_at: 2026-06-23

## 结论

SC-NMT 的历史 Codex 会话不能只做聊天摘要，应按 `inventory -> theme summary -> reusable knowledge / prompt / research asset / decision record -> registry update` 的链路沉淀。

该流程的核心价值是把历史过程转成可检索、可验证、可复用的 harness 资产，同时把未验证的科学判断保留为 `pending validation` 或 `hypothesis`。

## 适用条件

- 需要批量整理 `C:\Users\Administrator\.codex\sessions` 中与某个科研项目相关的历史会话。
- 目标项目有明确路径，例如 `G:\projects\SC-NMT`。
- 需要把过程沉淀到 `G:\BaiduSyncdisk\ResearchLoop` 和 `G:\knowledge`，而不是写入旧的 `G:\knowledge\_harness`。

## 步骤

1. 扫描 `rollout-*.jsonl` 会话文件。
2. 用 `session_meta.cwd`、用户消息、文件路径和关键词识别项目相关会话。
3. 生成 machine-readable inventory 和 human-readable inventory。
4. 按主题聚类，例如 calibration/projection、scatter/alignment、reconstruction、PPT、paper claim boundary、harness/memory。
5. 将可复用流程写入 `G:\knowledge\reusable_knowledge`。
6. 将可复用 prompt 写入 `G:\knowledge\reusable_prompts`。
7. 将原始素材清单写入当前项目 `research_assets\YYYYMMDD_task_name`。
8. 更新 `G:\BaiduSyncdisk\ResearchLoop\registry`。

## 关键参数

- scanned_session_files: 551
- matched_sc_nmt_sessions: 72
- primary_project: `G:\projects\SC-NMT`
- asset_dir: `G:\projects\SC-NMT\research_assets\20260623_sc_nmt_historical_sessions_ingestion`

## 风险

- 历史会话里出现的科学结论不能直接视为已验证结论。
- 原始 JSONL 不应复制到 knowledge，只能作为 evidence_refs 或项目内 research_assets 引用。
- 如果源会话本身存在 mojibake，整理卡片必须标注边界，不能伪造原始中文。

## 验证依据

- `session_inventory.json` 记录 72 个 SC-NMT 相关会话。
- `theme_summary.md` 记录六类主题及代表会话。
- `registry/knowledge.yaml`、`registry/prompts.yaml`、`registry/research_assets.yaml` 和 `registry/decisions.yaml` 已登记对应资产。

## 未验证边界

历史会话中的具体实验指标、PPT 质量判断、算法性能和论文 claim 仍需回到项目 artifacts、运行日志、图像证据和复现命令中逐项验证。
""",
    Path("G:/knowledge/reusable_knowledge/experimental_system/20260623_sc_nmt_calibration_projection_history.md"): r"""# SC-NMT 标定与投影几何历史会话沉淀

status: pending validation
source_project: sc-nmt
updated_at: 2026-06-23

## 结论

历史会话显示，SC-NMT 的标定与投影几何路线长期围绕 `view1/view4`、crop-origin、principal point、pose correction、small-pose correction、projection manifest 和 downstream approval 展开。

这些内容目前是历史过程沉淀，不是最终标定结论；正式论文或算法 claim 必须回到 calibration artifacts、projection matrices、QC 图和复现命令验证。

## 适用条件

- 整理 SC-NMT Phase 1 / Phase 1.5 / Phase 1.6 / Phase 2 中与投影几何相关的历史讨论。
- 需要判断某个 downstream reconstruction 是否使用了 active calibration artifact。
- 需要区分 full calibration、inferred geometry 和 downstream approval。

## 步骤

1. 确认 raw TIFF、crop、ROI 和 active calibration artifact 的对应关系。
2. 检查 projection package 是否包含 crop-origin、principal point、direction rule、pose correction 和 small-pose correction。
3. 用 contact sheet、detector hit、FOV bbox 或 reprojection diagnostic 做 sanity gate。
4. 只有在 artifact、manifest 和 approval 同时存在时，才把几何输入作为 formal observation package。

## 关键参数

- 历史会话主题计数：calibration_projection_geometry 22 sessions。
- 反复出现的校验尺度包括 5 mm 标定件、view1/view4、projection package 和 downstream approval。

## 风险

- 历史对话里出现的几何值不等价于当前 active calibration。
- 手工 approval 如果没有 reviewer、reviewed_at 和 artifact hash，不应提升为 validated。
- Phase 2 / Phase 3 的重建误差不能反推标定已经正确。

## 验证依据

- `G:\projects\SC-NMT\research_assets\20260623_sc_nmt_historical_sessions_ingestion\theme_summary.md`
- `G:\projects\SC-NMT\AGENTS.md` 中关于 `view1` / `view4` 和证据边界的规则。

## 未验证边界

仍需逐项核对 calibration summary、projection matrices、QC preview、manifest hash 和运行日志。
""",
    Path("G:/knowledge/reusable_knowledge/image_processing/20260623_sc_nmt_scatter_alignment_history.md"): r"""# SC-NMT 预处理与散射对齐历史会话沉淀

status: pending validation
source_project: sc-nmt
updated_at: 2026-06-23

## 结论

历史会话显示，SC-NMT 的预处理路线反复强调 scatter mask、manual approval、view mask、hash、256x256 / inner192 尺度、aligned observation package 和 ART 前输入一致性。

这些内容是历史流程边界，不是已验证图像处理结论；正式使用前必须核对 mask、QC 图、approval artifact 和下游重建输入 manifest。

## 适用条件

- 处理 P-011 或同类喷雾图像的 scatter gate、mask、ROI、alignment 和 observation package。
- 需要判断某个预处理输出能否进入 ART/SART/Mie 重建。

## 步骤

1. 检查输入图像、ROI、view split 和 mask 的来源。
2. 保存每个 view 的 mask、hash 和 manifest。
3. 对 scatter gate 进行 QC 预览，不把 `pending_manual_review` 当成 paper-grade evidence。
4. 在进入重建前确认 aligned observation package 的尺寸、视角顺序和权重定义。

## 关键参数

- 历史会话主题计数：preprocess_scatter_alignment 19 sessions。
- 常见尺度：`256x256_inner192`。
- 常见风险点：scatter gate、manual approval、mask hash、view order。

## 风险

- 只看预览图可能掩盖 mask 误删或漏删。
- 缺少 reviewer、reviewed_at、approved 和 accepted_override 的人工判断不能作为最终证据。
- 预处理坐标系错误会直接污染 ART/SART/Mie 结果。

## 验证依据

- `G:\projects\SC-NMT\research_assets\20260623_sc_nmt_historical_sessions_ingestion\theme_summary.md`
- `G:\projects\SC-NMT\docs\scatter_removal_workflow.md` 若存在，应作为后续核验入口。

## 未验证边界

仍需补齐每个 mask 的 QC 图、hash、approval artifact 和对应重建输入 manifest。
""",
    Path("G:/knowledge/reusable_knowledge/3d_reconstruction/20260623_sc_nmt_mie_art_reconstruction_history.md"): r"""# SC-NMT ART、Geo-SART、Mie-SART 与 Mie-Pk-TV-S 历史沉淀

status: pending validation
source_project: sc-nmt
updated_at: 2026-06-23

## 结论

历史会话显示，SC-NMT 的三维重建路线经历了 ART / Geo-SART / Mie-SART / Mie-Pk-TV-S 等阶段，并反复强调 Pk 投影、TV 正则、soft support、volume manifest、reprojection metrics 和 paper-ready claim boundary。

这些信息目前是路线沉淀和风险边界，不是最终算法性能声明。

## 适用条件

- 整理 SC-NMT Phase 2 / Phase 2.6 中关于 3D 重建、Mie 强度和 PPT/论文图的历史讨论。
- 判断某个重建输出是否只能作为 sanity evidence，还是可以进入 paper-ready evidence package。

## 步骤

1. 明确当前使用的是 sanity baseline、ART、Geo-SART、Mie-SART 还是 Mie-Pk-TV-S。
2. 保存 volume array、voxel grid metadata、manifest、reprojection metrics 和图像导出参数。
3. 不把 simplified geometry 的结果描述为真实 `3x4 P_k` projector 结论。
4. 对 PPT/论文图保留 10% / 20% / 30% isosurface、orthogonal slices 和 residual panel 等证据结构。

## 关键参数

- 历史会话主题计数：mie_art_reconstruction 11 sessions。
- 历史讨论中出现过 `137 x 144 x 136 = 2,683,008` voxels、`50 x 50 x 45 = 112,500` voxels、`W3=0.00`、`view3_rmse = 0.0631240827048565` 等线索。
- 上述数值必须回到对应 artifacts 后才能作为正式指标。

## 风险

- 将 sanity baseline 误称为 paper-ready reconstruction。
- 将 normalized voxel coordinates 误当成 mm 坐标。
- 将单视角或简化投影误扩展为完整多视角 Mie claim。

## 验证依据

- `G:\projects\SC-NMT\research_assets\20260623_sc_nmt_historical_sessions_ingestion\theme_summary.md`
- 历史会话中 Phase 2.6、metrics、volume export 和 PPT 输出的聚类记录。

## 未验证边界

仍需逐项核对运行日志、volume manifest、重投影残差、对比图、坐标系定义和论文 claim 文本。
""",
    Path("G:/knowledge/reusable_knowledge/scientific_visualization/20260623_sc_nmt_historical_visual_materials.md"): r"""# SC-NMT 历史 PPT 与科学可视化素材沉淀

status: validated
source_project: sc-nmt
updated_at: 2026-06-23

## 结论

SC-NMT 的历史会话中已经形成一条可复用科学可视化规则：科研 PPT 和论文图应优先使用真实数据图像本体，并用可编辑 PPT 图层承载文字、箭头、标注、色卡和解释元素。

该结论的 workflow 级别已经 validated；但每个具体 PPT 或 figure 是否达到论文级，仍需按分辨率、图层、数据来源和视觉审核逐项验证。

## 适用条件

- 制作 SC-NMT 的 Phase PPT、论文图、组会图或 GitHub/article 可视化素材。
- 需要从历史 PPT 经验中提取可复用审美和 prompt，而不是复制旧文件。

## 步骤

1. 先确认图像来源是真实数据、真实截图或明确标注的示意图。
2. 将文字、箭头、线条、框、色卡、图例和说明拆为可编辑图层。
3. 对 bitmap 按展示尺寸计算 effective dpi。
4. 将可复用 prompt 写入 `G:\knowledge\reusable_prompts\scientific_visualization`。
5. 将原始 PPT、预览图、脚本或素材清单保留在项目 `research_assets` 中。

## 关键参数

- 历史会话主题计数：scientific_visualization_and_ppt 9 sessions。
- 推荐比例：16:9。
- 论文级 bitmap 目标：effective dpi 通常应不低于 300。
- 推荐色图：perceptual sequential colormap；谨慎使用 rainbow/jet。

## 风险

- 用虚拟生成图替代真实观测图，会削弱科学证据链。
- 只保存最终 `.pptx` 而没有 preview/export evidence，会降低复现性。
- 过度美化可能遮蔽数据边界、mask 边界或 reconstruction status。

## 验证依据

- `G:\projects\SC-NMT\research_assets\20260623_sc_nmt_historical_sessions_ingestion\theme_summary.md`
- `G:\knowledge\reusable_knowledge\scientific_visualization\20260623_editable_scientific_ppt_closeout.md`

## 未验证边界

每个具体 PPT 或 figure 仍需单独检查真实数据来源、图层可编辑性、preview/export evidence 和 effective dpi。
""",
    Path("G:/knowledge/reusable_knowledge/paper_writing/20260623_sc_nmt_paper_claim_boundary_history.md"): r"""# SC-NMT 论文 claim boundary 历史沉淀

status: pending validation
source_project: sc-nmt
updated_at: 2026-06-23

## 结论

SC-NMT 历史会话反复强调一个边界：不能把 sanity baseline、诊断性预览、未核验 geometry 或简化 Mie 指标写成 paper-ready 结论。

可复用的写作策略是把 claim 分层：workflow evidence、diagnostic evidence、validated reconstruction evidence、paper claim 分开写，并明确哪些仍是 `pending validation`。

## 适用条件

- 撰写 SC-NMT Phase 2.6 / Phase 3 论文、组会汇报或阶段报告。
- 需要判断 Mie-Pk-TV-S、relative equivalent Mie scattering intensity、D32/SMD 或 3D morphology 是否能进入论文主张。

## 步骤

1. 将每条 claim 连接到 artifact、metric、figure、log 或 reproduction command。
2. 区分 relative equivalent Mie scattering intensity 与真实 Mie 物理反演量。
3. 将 sanity baseline、diagnostic/preflight result 和 final evidence 分开命名。
4. 对未验证内容使用 `hypothesis` 或 `pending validation`。

## 关键参数

- 历史会话主题计数：paper_readiness 9 sessions。
- 常见 figure 结构：10% / 20% / 30% isosurface、orthogonal slices、reprojection residual panel。
- claim 必须绑定 metadata、manifest 和复现入口。

## 风险

- 把 Phase 2/3 的探索结果过早写成 paper-ready 结论。
- 把相对强度、归一化坐标或简化几何误写成绝对物理量。
- 用 PPT 视觉效果替代科学验证。

## 验证依据

- `G:\projects\SC-NMT\research_assets\20260623_sc_nmt_historical_sessions_ingestion\theme_summary.md`
- ResearchLoop 中关于 `relative equivalent Mie scattering intensity` 和 claim boundary 的历史沉淀。

## 未验证边界

仍需与最终论文证据表、实验日志、运行指标和导师反馈逐项对齐。
""",
    Path("G:/knowledge/reusable_prompts/codex/20260623_batch_sc_nmt_session_ingestion_prompt.md"): r"""# Prompt Card: 批量 SC-NMT 历史 Codex 会话沉淀

status: validated
updated_at: 2026-06-23

## task

将 SC-NMT 历史 Codex 会话批量沉淀到 ResearchLoop、knowledge、research_assets 和 decision records。

## input

- `C:\Users\Administrator\.codex\sessions\**\rollout-*.jsonl`
- 当前主项目路径：`G:\projects\SC-NMT`
- canonical harness path：`G:\BaiduSyncdisk\ResearchLoop`
- reusable knowledge root：`G:\knowledge\reusable_knowledge`
- reusable prompts root：`G:\knowledge\reusable_prompts`

## output

- session inventory
- theme summary
- reusable knowledge cards
- prompt card
- research asset manifest
- decision record
- registry updates

## prompt body

你正在为 SC-NMT 做历史 Codex 会话沉淀。不要只总结聊天记录，要把每条高价值经验转成可触发、可检索、可验证、可复用的 harness asset。

请执行：

1. 读取 `G:\BaiduSyncdisk\ResearchLoop\AGENTS.md` 和 `harness.yaml`。
2. 扫描 `C:\Users\Administrator\.codex\sessions` 下的 `rollout-*.jsonl`。
3. 用 `session_meta.cwd=G:\projects\SC-NMT`、用户消息、文件路径和关键词识别 SC-NMT 相关会话。
4. 生成 machine-readable inventory 和 human-readable inventory。
5. 按主题聚类：calibration/projection、scatter/alignment、Mie/ART reconstruction、scientific visualization/PPT、paper claim boundary、harness/memory。
6. 对可复用内容生成 knowledge cards；未经验证的科学结论必须写为 `pending validation`。
7. 对可复用提示词生成 prompt card。
8. 对原始素材生成项目内 `research_assets\YYYYMMDD_task_name`，包含 `00_asset_manifest.md` 和 `reproduction_entry.md`。
9. 更新 ResearchLoop registry。
10. 运行 YAML 和路径验证，报告 evidence_refs、未验证边界和剩余风险。

## model

Codex Desktop / GPT-5 family

## notes

- 不复制原始 JSONL 到 knowledge。
- 不把 historical planning/review evidence 写成最终科学结论。
- 不写入 `G:\knowledge\_harness`。
- 所有 canonical harness 写入目标都是 `G:\BaiduSyncdisk\ResearchLoop`。

## revision history

| date | version | notes |
|---|---|---|
| 2026-06-23 | v1 | 用于 SC-NMT 72 个历史会话的批量沉淀。 |
| 2026-06-23 | v1.1 | 修复坏编码正文，明确 canonical harness path 和 pending validation 边界。 |
""",
    Path("G:/BaiduSyncdisk/ResearchLoop/decisions/20260623_grouped_historical_session_assetization.md"): r"""# Decision: SC-NMT 历史会话采用分组资产化沉淀

date: 2026-06-23
project_id: sc-nmt
status: validated
changed_route_or_assumption: true

## Decision

SC-NMT 历史 Codex 会话采用 inventory、主题聚类和按类别知识卡沉淀的方式处理。

具体做法是：先建立 `session_inventory` 和 `theme_summary`，再分别生成 reusable knowledge、reusable prompts、project research_assets 和 decision records，最后更新 ResearchLoop registry。

## Rationale

一次性把 72 个 SC-NMT 相关历史会话压缩成普通摘要，会丢失可复用的过程资产、验证边界和触发条件。

分组资产化能够保留：

- 哪些会话服务于 calibration/projection、scatter/alignment、reconstruction、PPT、paper claim boundary 或 harness/memory。
- 哪些内容是可复用 workflow。
- 哪些内容只是 historical evidence，必须保留为 `pending validation`。
- 哪些素材应该留在项目 `research_assets`，而不是复制到 knowledge。

## Rejected

- 将所有 JSONL 全量复制进 knowledge：体积大、噪声高，且容易污染可复用知识。
- 将每个会话都写成单独知识卡：维护成本过高，检索质量差。
- 将历史对话里的科学判断直接提升为 validated：缺少 artifact、metric、figure 和 reproduction evidence。

## Closeout Effect

- research goal：服务于 SC-NMT 长期科研记忆、可复用工作流和论文证据治理。
- project route：从 prose summary 转为 registry-backed assetization。
- system design：新增 historical session ingestion skill、prompt card 和 research asset manifest。

## Verification

- 扫描 551 个 session 文件。
- 识别 72 个 SC-NMT 相关会话。
- 生成 `session_inventory.json`、`session_inventory.md` 和 `theme_summary.md`。
- 更新 knowledge、prompts、research_assets 和 decisions registry。
""",
    Path("G:/BaiduSyncdisk/ResearchLoop/skills/historical_session_ingestion.md"): r"""# Historical Session Ingestion

## Purpose

将历史 Codex 会话沉淀为 ResearchLoop 可追踪资产，而不是普通聊天摘要。

该 skill 适用于 SC-NMT 或其他 G 盘科研项目的历史会话复盘。输出应进入 canonical harness：`G:\BaiduSyncdisk\ResearchLoop`，以及长期知识入口：`G:\knowledge\reusable_knowledge` 和 `G:\knowledge\reusable_prompts`。

## Procedure

1. 读取 `harness.yaml` 和 `AGENTS.md`。
2. 扫描 `C:\Users\Administrator\.codex\sessions\**\rollout-*.jsonl`。
3. 用 `session_meta.cwd`、路径、关键词和用户目标识别目标项目会话。
4. 生成 machine-readable inventory 和 human-readable inventory。
5. 按主题聚类。
6. 提取 reusable knowledge。
7. 提取 reusable prompts。
8. 将原始素材清单写入项目内 `research_assets`。
9. 生成或更新 decision records。
10. 更新 registry，并运行 validator、index rebuild 和 closeout_check。

## Quality Gates

- 不复制原始实验大数据到 knowledge。
- 不复制完整 JSONL 到 knowledge。
- 未验证科学结论必须标记为 `hypothesis` 或 `pending validation`。
- 只把可复用流程、参数、边界、风险和验证依据写入知识卡。
- 所有 registry 和 markdown 使用 UTF-8。

## Outputs

- `session_inventory.json`
- `session_inventory.md`
- `theme_summary.md`
- `00_asset_manifest.md`
- `reproduction_entry.md`
- reusable knowledge cards
- reusable prompt cards
- registry updates
- closeout health report
""",
    Path("G:/BaiduSyncdisk/ResearchLoop/reports/20260623_sc_nmt_historical_sessions_ingestion_report.md"): r"""# SC-NMT Historical Sessions Ingestion Report

```yaml
id: 20260623_sc_nmt_historical_sessions_ingestion_report
project_id: sc-nmt
status: validated
created_at: 2026-06-23
session_count: 72
```

## Summary

本次从 `C:\Users\Administrator\.codex\sessions` 中扫描 551 个 Codex session 文件，识别 72 个与 SC-NMT 相关的历史会话，并将这些过程沉淀为 inventory、theme summary、knowledge cards、prompt card、research asset manifest 和 decision record。

## Theme Counts

- calibration_projection_geometry: 22 sessions
- preprocess_scatter_alignment: 19 sessions
- mie_art_reconstruction: 11 sessions
- paper_readiness: 9 sessions
- scientific_visualization_and_ppt: 9 sessions
- harness_and_memory: 2 sessions

## Captured Files

- `G:\projects\SC-NMT\research_assets\20260623_sc_nmt_historical_sessions_ingestion\session_inventory.json`
- `G:\projects\SC-NMT\research_assets\20260623_sc_nmt_historical_sessions_ingestion\session_inventory.md`
- `G:\projects\SC-NMT\research_assets\20260623_sc_nmt_historical_sessions_ingestion\theme_summary.md`
- `G:\projects\SC-NMT\research_assets\20260623_sc_nmt_historical_sessions_ingestion\00_asset_manifest.md`
- `G:\projects\SC-NMT\research_assets\20260623_sc_nmt_historical_sessions_ingestion\reproduction_entry.md`

## Knowledge Cards

- `20260623_historical_session_ingestion_workflow`
- `20260623_sc_nmt_calibration_projection_history`
- `20260623_sc_nmt_scatter_alignment_history`
- `20260623_sc_nmt_mie_art_reconstruction_history`
- `20260623_sc_nmt_historical_visual_materials`
- `20260623_sc_nmt_paper_claim_boundary_history`

## Prompt And Harness Skill

- Prompt: `20260623_batch_sc_nmt_session_ingestion_prompt`
- Harness skill file: `G:\BaiduSyncdisk\ResearchLoop\skills\historical_session_ingestion.md`

## Verification

- 生成 session inventory。
- 更新 knowledge、prompts、research_assets 和 decisions registry。
- 后续通过 `registry_tool.py validate`、`kb_index.py rebuild` 和 `closeout_check.py` 复核。

## Boundaries

- 原始 session JSONL 不复制进 `G:\knowledge`。
- 历史会话里的科学判断不能直接写成确定结论；缺少 artifacts 和 metrics 的内容保持 `pending validation`。
- 本报告证明沉淀流程完成，不证明每个历史科研结论已经验证。
""",
    Path("G:/projects/SC-NMT/research_assets/20260623_sc_nmt_historical_sessions_ingestion/00_asset_manifest.md"): r"""# SC-NMT Historical Sessions Ingestion Asset Manifest

```yaml
id: 20260623_sc_nmt_historical_sessions_ingestion
project_id: sc-nmt
status: validated
created_at: 2026-06-23
```

## 素材清单

| 文件 | 类型 | 说明 |
|---|---|---|
| `session_inventory.json` | machine-readable inventory | 72 个 SC-NMT 相关历史会话的结构化清单。 |
| `session_inventory.md` | human-readable inventory | 供人工浏览的会话清单，包含主题与代表请求。 |
| `theme_summary.md` | theme summary | 按 calibration、scatter、reconstruction、PPT、paper、harness 等主题聚类。 |
| `G:\BaiduSyncdisk\ResearchLoop\reports\20260623_sc_nmt_historical_sessions_ingestion_report.md` | harness report | 本次历史会话沉淀的总结报告。 |

## 来源路径

- `C:\Users\Administrator\.codex\sessions\**\rollout-*.jsonl`
- `G:\projects\SC-NMT`

## 用途

- GitHub：提炼项目历史路线与可复用工程规则。
- Article / Paper / PPT：查找可追溯素材和历史证据线索。
- Codex retrieval：为后续 closeout、knowledge capture 和 prompt capture 提供索引入口。

## 复现入口

- `reproduction_entry.md`
- `G:\BaiduSyncdisk\ResearchLoop\skills\historical_session_ingestion.md`

## 证据

- 扫描 session 文件：551 个。
- 识别 SC-NMT 相关会话：72 个。
- 已更新 registry：knowledge、prompts、research_assets、decisions。

## 不得复制的大数据说明

本目录不复制原始实验 TIFF、`.npy`、`.pptx` 或完整 JSONL。原始 Codex sessions 仍保留在用户本机 session 目录；knowledge 只保存可复用结论、流程、prompt 和验证边界。
""",
    Path("G:/projects/SC-NMT/research_assets/20260623_sc_nmt_historical_sessions_ingestion/reproduction_entry.md"): r"""# Reproduction Entry: SC-NMT Historical Sessions Ingestion

```yaml
id: 20260623_sc_nmt_historical_sessions_ingestion_reproduction
project_id: sc-nmt
status: validated
created_at: 2026-06-23
```

## 目的

复现“从 Codex 历史 session 中识别 SC-NMT 相关工作，并沉淀到 ResearchLoop 与 `G:\knowledge`”的过程。

## 输入

- `C:\Users\Administrator\.codex\sessions\**\rollout-*.jsonl`
- `G:\projects\SC-NMT`
- `G:\BaiduSyncdisk\ResearchLoop\AGENTS.md`
- `G:\BaiduSyncdisk\ResearchLoop\harness.yaml`

## 流程

1. 扫描 `rollout-*.jsonl`。
2. 解析 `session_meta`、用户消息、文件路径和项目关键词。
3. 筛选 `cwd=G:\projects\SC-NMT` 或明显服务于 SC-NMT 的会话。
4. 按主题聚类：calibration、scatter、reconstruction、PPT、paper、harness。
5. 生成 `session_inventory.json`、`session_inventory.md` 和 `theme_summary.md`。
6. 生成 reusable knowledge、prompt card、decision record 和 registry updates。

## 输出

- `session_inventory.json`
- `session_inventory.md`
- `theme_summary.md`
- `00_asset_manifest.md`
- `G:\BaiduSyncdisk\ResearchLoop\reports\20260623_sc_nmt_historical_sessions_ingestion_report.md`

## 验证命令

```powershell
python G:\BaiduSyncdisk\ResearchLoop\scripts\registry_tool.py validate
python G:\BaiduSyncdisk\ResearchLoop\scripts\kb_index.py rebuild
python G:\BaiduSyncdisk\ResearchLoop\scripts\closeout_check.py
```

## 边界

该复现入口验证历史会话沉淀流程，不验证每个历史科研结论。历史会话里的算法指标、图像判断和论文 claim 必须回到 SC-NMT 项目 artifacts 中再次验证。
""",
}


REGISTRY_IDS = {
    "knowledge": {
        "20260623_historical_session_ingestion_workflow",
        "20260623_sc_nmt_calibration_projection_history",
        "20260623_sc_nmt_scatter_alignment_history",
        "20260623_sc_nmt_mie_art_reconstruction_history",
        "20260623_sc_nmt_historical_visual_materials",
        "20260623_sc_nmt_paper_claim_boundary_history",
    },
    "prompts": {"20260623_batch_sc_nmt_session_ingestion_prompt"},
    "research_assets": {"20260623_sc_nmt_historical_sessions_ingestion"},
    "decisions": {"20260623_grouped_historical_session_assetization"},
}


def update_registries() -> list[str]:
    changed: list[str] = []
    stamp = now_iso()
    for name, ids in REGISTRY_IDS.items():
        data = read_yaml(REGISTRY_FILES[name])
        items = data.get(name, [])
        for item in items:
            item_id = str(item.get("id") or item.get("project_id") or "")
            if item_id not in ids:
                continue
            if item.get("encoding_status") != "ok":
                item["encoding_status"] = "ok"
                changed.append(f"{name}:{item_id}:encoding_status")
            item["encoding_repaired_at"] = stamp
        write_yaml(REGISTRY_FILES[name], data)
    return changed


def main() -> int:
    repaired_files: list[str] = []
    for path, content in REPAIRS.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if not content.endswith("\n"):
            content += "\n"
        path.write_text(content, encoding="utf-8")
        repaired_files.append(str(path))

    registry_changes = update_registries()
    report = Path("G:/BaiduSyncdisk/ResearchLoop/reports/health/20260623_encoding_repair.md")
    report.write_text(
        "# Encoding Repair Report 20260623\n\n"
        "## Repaired Files\n\n"
        + "\n".join(f"- `{path}`" for path in repaired_files)
        + "\n\n## Registry Updates\n\n"
        + ("\n".join(f"- `{item}`" for item in registry_changes) if registry_changes else "- none")
        + "\n\n## Boundary\n\n"
        "Raw inventory JSON and raw historical request excerpts were not rewritten as scientific evidence. "
        "This repair only rebuilds reusable markdown cards, prompt, skill, report, manifest and reproduction entry.\n",
        encoding="utf-8",
    )
    append_ledger(
        "encoding_artifact_repair",
        {
            "repaired_file_count": len(repaired_files),
            "repaired_files": repaired_files,
            "registry_changes": registry_changes,
            "report": str(report),
        },
    )
    print(f"repaired_file_count={len(repaired_files)}")
    print(f"report={report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
