import fs from "node:fs/promises";
import { createRequire } from "node:module";

const runtimePackage = "C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json";
const require = createRequire(runtimePackage);
const { FileBlob, SpreadsheetFile } = require("@oai/artifact-tool");

const workbookPath = "D:/2026.9.21_finally/Agents/PA12实验数据处理/实验概览/PA12实验概览_汇总.xlsx";
const previewPath = "D:/2026.9.21_finally/.codex-pa12-overview-preview.png";

const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(workbookPath));
const sheet = workbook.worksheets.getItemAt(0);
const used = sheet.getRange("A1:I11");

sheet.showGridLines = false;
used.format.font = { name: "Arial", size: 10, color: "#222222" };
used.format.verticalAlignment = "center";
used.format.wrapText = false;
sheet.getRange("A1:I1").format = {
  fill: "#1F4E78",
  font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" },
  horizontalAlignment: "center",
  verticalAlignment: "center",
};
sheet.getRange("A2:A11").format.horizontalAlignment = "left";
sheet.getRange("B2:I11").format.horizontalAlignment = "right";
sheet.getRange("A1:I11").format.borders = {
  insideHorizontal: { style: "thin", color: "#D9E2F3" },
  bottom: { style: "thin", color: "#A6A6A6" },
};
sheet.getRange("A1:I1").format.rowHeight = 24;
sheet.getRange("A2:I11").format.rowHeight = 20;

const widths = [14, 12, 12, 12, 15, 12, 15, 14, 14];
for (let index = 0; index < widths.length; index += 1) {
  sheet.getRangeByIndexes(0, index, 11, 1).format.columnWidth = widths[index];
}
sheet.freezePanes.freezeRows(1);

workbook.recalculate();
const preview = await workbook.render({ sheetName: sheet.name, range: "A1:I11", scale: 1.5, format: "png" });
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(workbookPath);

const check = await workbook.inspect({
  kind: "table",
  range: `${sheet.name}!A1:I11`,
  include: "values,formulas",
  tableMaxRows: 11,
  tableMaxCols: 9,
});
console.log(check.ndjson);
