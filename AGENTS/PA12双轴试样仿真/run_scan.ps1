$ErrorActionPreference = 'Stop'

$abaqus = 'D:\SIMULIA\Commands\abaqus.bat'
$vaultAlias = 'C:\yuan_sb'
$dataAlias = 'C:\yuan_data'
if (-not (Test-Path $vaultAlias)) {
    New-Item -ItemType Junction -Path $vaultAlias -Target 'D:\C盘迁移\Desktop\yuan\second brain' | Out-Null
}
if (-not (Test-Path $dataAlias)) {
    New-Item -ItemType Junction -Path $dataAlias -Target 'D:\C盘迁移\Desktop\yuan\data' | Out-Null
}
$script = Join-Path $vaultAlias 'AGENTS\PA12双轴试样仿真\pa12_biaxial_scan.py'
$modelDir = Join-Path $dataAlias 'XY\picture-20250529\vertical_all_45°\moxing'
$runRoot = Join-Path $vaultAlias 'AGENTS\PA12双轴试样仿真\runs'
$runtimeInputRoot = 'C:\pa12_inputs'
$runtimeOutputRoot = 'C:\pa12_results'
$runtimeScript = 'C:\pa12_biaxial_scan.py'
if (-not (Test-Path $runtimeInputRoot)) {
    New-Item -ItemType Directory -Path $runtimeInputRoot | Out-Null
}
if (-not (Test-Path $runtimeOutputRoot)) {
    New-Item -ItemType Directory -Path $runtimeOutputRoot | Out-Null
}
Copy-Item -LiteralPath $script -Destination $runtimeScript -Force

function Get-ShortPath([string]$Path) {
    $line = 'for %I in ("{0}") do @echo %~sI' -f $Path
    (cmd.exe /d /c $line).Trim()
}

New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
$scriptNoExtension = 'C:\pa12_biaxial_scan'

$models = @(
    @{ Name = 'a3p0'; File = '01_a3p0mm.step'; Thickness = 3.0 },
    @{ Name = 'a2p5'; File = '02_a2p0.25mm.step'; Thickness = 2.5 },
    @{ Name = 'a2p0'; File = '03_a2p0.5mm.step'; Thickness = 2.0 },
    @{ Name = 'a1p5'; File = '04_a1p0.75mm.step'; Thickness = 1.5 },
    @{ Name = 'a1p0'; File = '05_a1p1.00mm.step'; Thickness = 1.0 }
)

foreach ($model in $models) {
    $step = Join-Path $modelDir $model.File
    $runtimeStep = Join-Path $runtimeInputRoot $model.File
    Copy-Item -LiteralPath $step -Destination $runtimeStep -Force
    $out = Join-Path $runtimeOutputRoot $model.Name
    $vaultOut = Join-Path $runRoot $model.Name
    New-Item -ItemType Directory -Path $out -Force | Out-Null
    Push-Location 'C:\'
    & $abaqus cae noenvstartup "noGUI=$scriptNoExtension" -- --step $runtimeStep --out $out --dx 0.5 --dy 0.5 --mesh 1.0
    Pop-Location
    if ($LASTEXITCODE -ne 0) {
        throw "Abaqus input generation failed for $($model.Name)"
    }
    New-Item -ItemType Directory -Path $vaultOut -Force | Out-Null
    Copy-Item -Path (Join-Path $out '*') -Destination $vaultOut -Recurse -Force
}
