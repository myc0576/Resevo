# Feedback Loop Rules

状态：`pending validation`

## Loop

每个科研任务结束时执行：

```text
goal alignment -> process review -> verification -> capture -> registry update -> next-task hints
```

## Rules

- 先判断是否值得沉淀，再写文件。
- 先确认验证证据，再决定状态字段。
- 先保留原始素材和复现入口，再考虑精修展示材料。
- 若任务改变路线、假设或系统设计，必须写 decision record。
- 如果没有可复用输出，只在最终报告中说明 closeout 检查结果，不强行创建 knowledge 或 prompt。

## Evidence Boundary

可以作为验证证据的材料包括：

- 指标。
- 残差。
- 相关系数。
- 对比图。
- 运行日志。
- 复现命令。
- 可追溯的源文件和输出路径。

未经验证的判断不能写成确定结论。
