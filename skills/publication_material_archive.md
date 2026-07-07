# Publication Material Archive

用途：归档与论文、PPT、文章、GitHub 或短视频相关的可复用科研素材。

## Trigger

当任务产生以下材料时使用：

- 论文图原始素材。
- PPT 可编辑素材。
- 可公开展示的过程图。
- 文章插图。
- GitHub 说明图。
- 视频脚本或演示素材。

## Procedure

1. 判断材料是否有科研证据边界。
2. 若是当前项目素材，优先放入当前项目 `research_assets\YYYYMMDD_task_name`。
3. 生成 `00_asset_manifest.md` 和 `reproduction_entry.md`。
4. 若材料对应可复用知识，同时写 knowledge card。
5. 更新 `registry\research_assets.yaml`。

## Boundary

不要把临时截图、不可追溯图片或大体量原始数据塞进 knowledge。
