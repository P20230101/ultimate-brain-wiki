# PA12 自建 VFM 阶段 I：单轴机器轴与 DIC 轴映射复核

## 目的与成功标准

消除单轴计算无条件继承双轴旋转映射的问题。每组单轴显式指定机器 X/Y 对应的 DIC x/y 轴；同一映射必须同时控制应变分量、虚场加载方向长度和载荷截面长度。结果重算后，单轴仍保持 `REVIEW_REQUIRED`，不得因拟合数值可用而升级为正式材料参数。

## 方法

对每个机器方向，DIC 应变取其显式映射分量；虚场长度沿该方向，边界应力面积中的边长取正交方向。等双轴十字试样继续使用已确认映射：机器 X→DIC y、机器 Y→DIC x。单轴按实验配置读取映射，不再隐式调用双轴规则。

机器轴—DIC 变换仍属于单轴工作候选，状态与证据随结果 JSON 输出。映射候选不会覆盖原始 DIC、力或同步数据。

## 方向证据与候选配置

- S19–S21：三组照片中的长条试样长轴沿图像竖直方向；当前候选为机器 X→DIC y、机器 Y→DIC x。照片朝向没有完成机器传感器、夹具和 Job 坐标的正式标定，状态为 `CANDIDATE_UNVERIFIED`。
- S22：照片显示上下夹持，Job ROI 约 `10.166626×44.333156 mm`、长边沿 DIC y；候选为机器 Y→DIC y、机器 X→DIC x。证据状态为 `IMAGE_SUPPORTED_NEEDS_COORDINATE_CONFIRMATION`，仍未通过设备坐标标定。

外部 S16 FE–DIC 预检记载 S16 双轴机器 X 为图像竖直、机器 Y 为图像水平，FE X/Y 分别对应 DIC `exx/eyy`；这一证据与双轴十字试样的既有映射一致，并已归档于 [`raw/PA12_Stage2_Evidence/`](../../../../raw/PA12_Stage2_Evidence/)。S16 是双轴十字试样，不是 S19–S22 长条单轴试样，故不能用它替代单轴逐试样坐标标定。

## 重算结果

全批自建 VFM 重算完成。S19–S21 的候选映射与此前双轴映射相同，数值保持不变；S22 映射和受力边长同步调整：

| 实验 | 机器轴→DIC轴候选 | 条件 E/MPa | 条件 Y/MPa | 条件 H/MPa | 积分面积比最低值 | 状态 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| S19_X_0.2 | X→y；Y→x | 5389.40 | 8.94 | 23357.94 | 0.870952 | REVIEW_REQUIRED |
| S20_X_2 | X→y；Y→x | 17600.49 | 41.74 | 18526.97 | 0.846928 | REVIEW_REQUIRED |
| S21_X_20 | X→y；Y→x | 16912.33 | — | — | 0.867534 | REVIEW_REQUIRED |
| S22_Y_0.2 | X→x；Y→y | 10535.04 | 103.58 | 238.04 | 0.826930 | REVIEW_REQUIRED |

`E` 使用工作假设 `ν=0.375`；Y/H 来自当前约化阶段 2，不是 MatchID 材料识别结果。S22 在旧映射下的 E 为非正值，新候选映射下转为正值，表明方向与截面长度对参数反演有实质影响；这不能单独证明新候选正确。全部单轴面积比低于配置的 `0.95` 门槛，单轴几何与外功门槛也未通过，所有数值只作条件诊断。

## 验证

- 回归覆盖默认等双轴映射、显式竖直单轴映射、虚场长度/受力边长度关系、逐实验 S22 映射配置，以及完整小型合成单轴处理对阶段 2 应变/虚功映射的影响。
- 独立复核 S22 首个加载帧 `000016.jpg`：`Fy=175.3 N`、横向边长 `Lx=10.166626 mm`、中心厚度工作值 `1 mm`，输出 `σy=17.24269192 MPa`，与 `Fy/(t·Lx)` 一致；Y 虚场方向使用 ROI 纵向长度 `Ly=44.333156 mm`。
- 全量测试：`104 passed`。
- `compileall`：通过。
- 自建 VFM 输出：8 组可分析实验均保持 `SELF_VFM_REVIEW_REQUIRED`；S23/S24 继续由输入状态阻断。
- 输出契约审计通过，正式 VFM 总门槛仍为未就绪；应力—应变审计仍保留 `REVIEW_REQUIRED` 项。
- 原始 JPG、DAT、XLS 未修改。

## 尚未通过的门槛

1. S19–S22 机器传感器/夹具到 Job/DIC 坐标的逐试样标定。
2. 单轴厚度、有效宽度、标距、Polygon 对应的物理积分域和有向外功边界。
3. DIC 积分面积覆盖率及边界载荷与积分域的物理对应。
4. 独立泊松比约束、弹性窗口确认、阶段 1/2 稳定性和跨实验留出验证。

## 复现

```powershell
python -m pytest -q
python -m compileall -q tools tests
python tools/run_pa12_self_vfm.py --batch-config configs/pa12_rotated_batch.json --config configs/pa12_self_vfm.json
python tools/audit_pa12_outputs.py --config configs/pa12_rotated_batch.json
python tools/audit_pa12_stress_strain.py --config configs/pa12_rotated_batch.json
```

## 来源

- [机器轴映射配置](../../../../configs/pa12_self_vfm.json)
- [VFM runner](../../../../tools/run_pa12_self_vfm.py)
- [虚功和边界映射函数](../../../../tools/pa12_self_vfm.py)
- [外部 S16 FE–DIC 坐标预检](../../../../raw/PA12_Stage2_Evidence/阶段2_G4_S16_FE-DIC坐标映射预检.md)
- [阶段 B 单轴 Polygon 复核](PA12自建VFM阶段B单轴Polygon复核.md)
- [阶段 G S22 横向应变诊断](PA12自建VFM阶段G S22单轴横向应变诊断.md)
- [阶段 H 双轴 ROI 与厚度门槛](PA12自建VFM阶段H双轴ROI与厚度几何门槛.md)
