# MatchID VFM 准备包

这里保存进入 MatchID VFM 前的轻量索引、字段映射、审计结果和逐帧合并状态。

## 本机保留但不提交 GitHub 的文件

`<实验编号>/merged/` 下的逐帧 `DIC全场—力.csv` 是 MatchID 全场数据，当前批次约 5 GB。它们仍保留在本机 Vault，供 MatchID 和后续 VFM 使用；Git 忽略这些文件，避免把大型派生数据写入仓库历史。

`_matchid_export/` 是用于重构/交叉验证的 MatchID 原始 CSV 导出副本，也只保留在本机。

## GitHub 中保留的入口

- `PA12_MatchID_VFM实验级索引.csv`：每个实验的输入、帧数和闭环状态。
- `PA12_MatchID_VFM闭环状态.json/.md`：机器可读和人类可读的门禁状态。
- `PA12_DIC_DAT质量审计.*`：逐帧 DAT 字段可用性审计。
- `<实验编号>_帧—力—时间索引.csv`：照片主索引、同步时间和 X/Y 力。
- `<实验编号>/<实验编号>_DIC全场—力状态.json`：逐实验合并状态和失败原因。
- `../处理记录/PA12_GPT交接文档.md`：下一次 GPT 的工作入口。

重新生成本机大文件的入口：

```powershell
python tools/matchid_prepare.py --config configs/pa12_rotated_batch.json
python tools/merge_matchid_exports.py --config configs/pa12_rotated_batch.json --experiment S16_XY_0.2
```

只有在实验闭环状态为 `MATCHID_VFM_INPUT_READY`、边界载荷和坐标定义确认后，才进入 MatchID VFM 和 J2 参数识别。
