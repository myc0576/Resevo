# Paper Lifecycle Workflow

本 workflow 把 research project 从第一天绑定到 output object。论文是主线对象，但同一证据链可以继续生成 GitHub release、数据/代码包、组会 PPT、README、自媒体和科普素材。

## 0-1 使用方式

1. 在 `registry/output_objects.yaml` 新建 output object，写明输出类型、目标 venue、项目根目录和当前状态。
2. 在项目目录复制 `templates/research_project/` 的 00-08 模板。
3. 先填 `00_research_brief.md`、`01_target_paper_distillation.md`、`02_gap_and_contribution.md`。
4. 用 `03_claim_evidence_matrix.yaml` 把 central claim 拆成 claim、experiment、figure、data、code 和 reproduction command。
5. 用 `05_figure_registry.yaml` 管理每张图的 target message、claim_id、输入数据、脚本、输出路径和质量迭代。
6. 完成 manuscript、release、dissemination 后填写 `research_retro.md`。
7. 从 retro 生成 candidate assets，写入 `registry/asset_evolution.yaml`。
8. 通过 reuse gate 后，candidate 才能晋升 reusable。

## Gates

Gates 定义在 `paper_state_machine.yaml`；机器可检查规则在 `validation_rules.yaml`。

- `idea_gate`: 有明确 gap 和目标 venue。
- `design_gate`: 每条 claim 有 evidence plan。
- `experiment_gate`: raw/intermediate/results 和代码入口可追踪。
- `figure_gate`: 每张图服务 claim。
- `manuscript_gate`: 每节服务中心贡献。
- `release_gate`: README、LICENSE、CITATION、release notes、DOI 和复现命令可发布。
- `dissemination_gate`: 同一证据链能派生 PPT、README、自媒体素材。
- `asset_candidate_gate`: closeout 内容默认进入 candidate，不直接 reusable。
- `reuse_gate`: reusable 必须有 asset card、适用边界、复现入口和真实使用来源。
- `asset_deprecation_gate`: deprecated/replaced 必须保留历史和替代关系。
- `workflow_improvement_gate`: workflow 改进必须来自 retro、failed run、review feedback 或 validator failure。
- `closeout_gate`: 沉淀 reusable knowledge/prompts/assets/decisions 并更新 registry。

## Validation

```powershell
python scripts\validate_research_project.py --project-root examples\paper_lifecycle_minimal --json
```

该命令只检查结构、字段、状态枚举和复现入口，不解释具体实验参数。
