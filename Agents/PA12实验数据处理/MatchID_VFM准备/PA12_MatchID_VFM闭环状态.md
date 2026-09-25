# PA12 MatchID VFM 闭环状态

本文件把同步力值、DAT 全场记录、Job 覆盖和 Results Viewer 导出分开判断。同步力值通过不等于 MatchID VFM 输入已经完成。

- 正式 MatchID VFM 输入已闭合：`否`

| 实验 | 力值状态 | DAT 状态 | Job 状态 | 导出状态 | 当前状态 | 选定帧 | DAT 可用帧 | DAT 不可用帧 |
| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: |
| S15_XY_0.2 | FORCE_SYNC_READY | DIC_DAT_READY | JOB_COVERAGE_COMPLETE | MATCHID_VFM_INPUT_READY | MATCHID_VFM_INPUT_READY | 284 | 284 | 0 |
| S16_XY_0.2 | FORCE_SYNC_READY | DIC_DAT_READY | JOB_COVERAGE_COMPLETE | MATCHID_VFM_INPUT_READY | MATCHID_VFM_INPUT_READY | 257 | 257 | 0 |
| S17_XY_20 | FORCE_SYNC_READY | DIC_DAT_READY | JOB_COVERAGE_COMPLETE | MATCHID_VFM_INPUT_READY | MATCHID_VFM_INPUT_READY | 12 | 12 | 0 |
| S18_XY_2 | FORCE_SYNC_READY | DIC_DAT_READY | JOB_COVERAGE_COMPLETE | MATCHID_VFM_INPUT_READY | MATCHID_VFM_INPUT_READY | 126 | 126 | 0 |
| S19_X_0.2 | FORCE_SYNC_READY | DIC_DAT_READY | JOB_COVERAGE_COMPLETE | MATCHID_VFM_INPUT_READY | MATCHID_VFM_INPUT_READY | 126 | 126 | 0 |
| S20_X_2 | FORCE_SYNC_READY | DIC_DAT_READY | JOB_COVERAGE_COMPLETE | MATCHID_VFM_INPUT_READY | MATCHID_VFM_INPUT_READY | 63 | 63 | 0 |
| S21_X_20 | FORCE_SYNC_READY | DIC_DAT_READY | JOB_COVERAGE_COMPLETE | MATCHID_VFM_INPUT_READY | MATCHID_VFM_INPUT_READY | 36 | 36 | 0 |
| S22_Y_0.2 | FORCE_SYNC_READY | DIC_DAT_READY | JOB_COVERAGE_COMPLETE | MATCHID_VFM_INPUT_READY | MATCHID_VFM_INPUT_READY | 223 | 223 | 0 |
| S23_Y_2 | FORCE_SYNC_VISUAL_FRACTURE_FORCE_MISSING | DIC_DAT_READY | JOB_COVERAGE_COMPLETE | EXPORT_NOT_RUN | FORCE_REVIEW_REQUIRED | 191 | 191 | 0 |
| S24_Y_20 | FORCE_SYNC_PRELOAD_RELEASE_ONLY | DIC_NOT_INDEXED | JOB_COVERAGE_COMPLETE | EXPORT_NOT_RUN | PRELOAD_RELEASE_ONLY | 0 | 0 | 0 |

## 状态含义

- `FORCE_SYNC_READY`：照片—力同步 CSV 已通过当前力值契约。
- `FORCE_SYNC_VISUAL_FRACTURE_FORCE_MISSING`：照片已确认视觉断裂，但力文件在断裂前结束；不能补造断裂力或发布正式 VFM。
- `DIC_DAT_READY`：选定 DAT 均含 `<18>` 和 `<53>` 记录；逐字段映射已由同版本 Results Viewer 与同帧 DAT 交叉验证，映射写在各实验元数据 JSON。
- `JOB_COVERAGE_REVIEW_REQUIRED`：当前 Job 未覆盖全部选定照片，需要在 Results Viewer 重新导出或确认覆盖。
- `EXPORT_REQUIRED`：缺少导出且对应 DAT 不能重构，或仍有缺失帧；不能生成正式合并索引。
- `EXPORT_INVALID`：导出和对应 DAT 都不能满足字段契约，或 DAT 无法重构；不能填零、插值或静默删点。
- `MATCHID_VFM_INPUT_READY`：逐帧导出 CSV 或 DAT 重构结果已按声明字段、单位和同步力合并；这仍不是材料参数识别完成。

## 旋转后 VFM 边界约定

- 原始机器右上/左下为 `Y1/Y2`，右下/左上为 `X1/X2`；正式旋转 DIC 的边界映射为：顶部=`X2`、底部=`X1`、左侧=`Y2`、右侧=`Y1`。
- MatchID Boundary 顺序固定为 `0=顶部、1=左侧、2=右侧、3=底部`；双轴使用 X 顶/底、Y 左/右，单轴只使用受力方向两边；拉伸力为正。
- 外围夹持/加载结构厚度记录为 `3 mm`；中心 ROI 完全位于 `1 mm` 减薄区，MatchID 工程厚度用 `1 mm`。用户确认外围机器力传感器读数直接作为 ROI 边界合力输入 MatchID 自带 VFM。
- 所有当前双轴均为等双轴，按 `0.2、2、20 mm/s` 分速率识别；不要求非等双轴路径，也不恢复四边牵引分布。
- 阶段 1 固定 `ν=0.375` 识别 `E`；阶段 2 固定该 `E、ν` 识别屈服 `Y` 与硬化 `H`。闭环状态通过不等于 VFM 参数识别完成。

## 下一步

1. 先处理 `FORCE_REVIEW_REQUIRED`、`DIC_DAT_REVIEW_REQUIRED` 和 `JOB_COVERAGE_REVIEW_REQUIRED`。
2. 检查各实验合并状态中的 `DIC数据来源`、`DAT原始点数` 和 `排除无效点数`；确认 `DAT_RECONSTRUCTED` 仅排除了 DAT 明确标记为无效的点。
3. 对 `EXPORT_REQUIRED`、`EXPORT_INVALID` 和 `DIC_DAT_REVIEW_REQUIRED` 的实验回到 MatchID 处理，不能用力值数量相等代替 DIC 全场完整性。
4. 先按等双轴 VFM 当前检查结果核对 ROI 位置/尺寸、厚度、旋转后 XY、逐帧力同步、首帧零力和断裂/末帧对应；MatchID 参考图若为加载前零力帧，应单独核对其帧序映射。
5. 每个速度分开运行 MatchID 自带 VFM；记录内外虚功、残差、参数是否撞界和收敛状态。没有数值输出的字段写未识别/未计算。
