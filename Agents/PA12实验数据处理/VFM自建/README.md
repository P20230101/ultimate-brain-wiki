# PA12 自建 VFM 输出

本目录是 MatchID VFM 不可直接完成或需要独立复核时的可复现替代路径。它使用已经完成时间同步的 DIC 全场—Press 合并数据，不修改原始 JPG、DAT、XLS。

## 当前方法

1. 仅处理当前几何证据足够的等双轴十字试样；单轴长条试样暂不计算。
2. 旋转后的 DIC 坐标中，机器 X 方向使用 `Eyy` 和竖直边界长度，机器 Y 方向使用 `Exx` 和水平边界长度。
3. `X=(X1_Press+X2_Press)/2`，`Y=(Y1_Press+Y2_Press)/2`；中心厚度使用 1 mm，外围 3 mm 仅作记录。
4. 阶段 1 固定 `ν=0.375`，用常应变虚场和加载初期内外虚功识别 `E`。
5. 阶段 2 固定阶段 1 的 `E、ν`，用平面应力等效应力和 DIC 应变识别 `Y、H`，并导出 Linear、Ludwik、Swift、通用 Voce I/II 对比。

## 输出

每个实验目录包含：

- `内外虚功.csv/.png`：实验外功、阶段 1 内功和阶段 2 本构内功；
- `模型对比.csv`：等效塑性应变、等效应力和五类通用硬化模型；
- `应力空间.csv/.png`：双轴应力状态；
- `参数收敛.csv/.png`：累计拟合得到的 E、Y、H 稳定性；
- `结果.json`：机器可读的阶段状态、参数、质量门槛和限制。

汇总文件位于 `汇总/`。`SELF_VFM_CANDIDATE` 只是当前数据门槛下的候选结果，不等于 MatchID 或论文最终材料参数。

## 复现

```powershell
python tools/run_pa12_self_vfm.py --batch-config configs/pa12_rotated_batch.json --config configs/pa12_self_vfm.json
```

## 重要边界

- S15 的 ROI 与真实 1 mm 厚度过渡边界仍需人工核对。
- S23 力数据早于视觉断裂结束，不能补造断裂力。
- S24 是预载释放记录，不是完整拉伸实验。
- Voce I/II 在本目录中是通用文献形式，不声称等同于 MatchID 同名模型；接入 MatchID 前必须核对软件公式和参数定义。
