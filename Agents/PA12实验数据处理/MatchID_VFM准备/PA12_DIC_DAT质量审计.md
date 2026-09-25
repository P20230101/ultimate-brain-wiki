# PA12 DAT 逐帧质量审计

本报告审计同一照片索引下的 `.jpg.dat` 文件是否存在及是否包含 MatchID 记录。字段映射已通过同版本 MatchID 2D 19.2.2.0 Results Viewer 与同帧 DAT 交叉验证；这不是官方 DAT 格式文档。

## 状态统计

- `DIC_FIELDS_AVAILABLE`：`1318` 帧。

## 不可直接进入 DIC 全场合并的帧

- 无。

## 判定边界

- `DIC_FIELDS_AVAILABLE` 表示 `<18>` 和 `<53>` 均有记录；逐字段映射以各实验元数据 JSON 的 `dat.raw_field_map` 为准。
- `Job` 中是否列出照片单独记录；Job 缺帧不能覆盖 DAT 的实际记录状态。
