# Research Asset Harvest

用途：保留可用于 GitHub、Douyin、article、paper figure、PPT 的原始素材和复现入口。

## Trigger

当任务产生可展示、可复用或可追溯的素材时使用。

## Procedure

1. 在当前项目创建 `research_assets\YYYYMMDD_task_name`。
2. 保留原始素材或轻量引用说明，不复制原始实验大数据。
3. 创建 `00_asset_manifest.md`。
4. 创建 `reproduction_entry.md`。
5. 更新 `registry\research_assets.yaml`。

## Required Files

- `00_asset_manifest.md`：记录素材清单、来源路径、用途、验证证据和大数据边界。
- `reproduction_entry.md`：记录复现入口、命令、依赖、输入和输出。

## Boundary

不需要精修。优先保留可追溯性和复现入口。
