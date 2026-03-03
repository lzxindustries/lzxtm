#!/usr/bin/env pwsh
# Deploy script for LZX Technical Manual
# Uses a persistent local clone of the deploy repo to enable incremental pushes,
# avoiding GitHub's 2 GB pack size limit.
# Large image directories are committed and pushed in batches.

$ErrorActionPreference = 'Stop'

$root       = "c:\Users\lars\lzxtm"
$buildDir   = "$root\build"
$deployRepo = "$root\.deploy-repo"
$repoUrl    = "git@github.com:lzxindustries/lzxindustries.github.io.git"
$branch     = "main"
$vmImgRel   = "img\instruments\videomancer"  # large dir to batch

# 1. Build
Write-Host "`n=== Building site ===" -ForegroundColor Cyan
Push-Location $root
npm run build
if ($LASTEXITCODE -ne 0) { Pop-Location; throw "Build failed." }
Pop-Location

# 2. Ensure persistent deploy repo clone exists
if (Test-Path "$deployRepo\.git") {
    Write-Host "`n=== Updating existing deploy repo ===" -ForegroundColor Cyan
    Push-Location $deployRepo
    git fetch origin $branch
    git reset --hard "origin/$branch"
    Pop-Location
} else {
    Write-Host "`n=== Cloning deploy repo ===" -ForegroundColor Cyan
    if (Test-Path $deployRepo) { Remove-Item $deployRepo -Recurse -Force }
    git clone --branch $branch $repoUrl $deployRepo
}

# 3. Mirror build output into deploy repo, EXCLUDING the large videomancer images
Write-Host "`n=== Syncing build output (excluding $vmImgRel) ===" -ForegroundColor Cyan

# Remove all tracked content except .git and the videomancer img dir (handled separately)
Push-Location $deployRepo
Get-ChildItem -Force | Where-Object { $_.Name -ne '.git' } | Remove-Item -Recurse -Force
Pop-Location

# Copy everything except videomancer images
robocopy "$buildDir" "$deployRepo" /E /XD "$buildDir\$vmImgRel" /NFL /NDL /NJH /NJS /NC /NS /NP | Out-Null

# 4. Commit and push everything except videomancer images
Write-Host "`n=== Committing base content ===" -ForegroundColor Cyan
$sourceCommit = (git -C $root rev-parse --short HEAD)
Push-Location $deployRepo
git add --all
$status = git status --porcelain
if ($status) {
    git commit -m "Deploy website (base) - based on $sourceCommit"
    Write-Host "=== Pushing base content ===" -ForegroundColor Cyan
    git push origin $branch
    if ($LASTEXITCODE -ne 0) { Pop-Location; throw "Base push failed." }
} else {
    Write-Host "No base changes." -ForegroundColor Yellow
}
Pop-Location

# 5. Batch-copy and push videomancer images in chunks (~1.2 GB each)
Write-Host "`n=== Syncing videomancer images in batches ===" -ForegroundColor Cyan
$vmBuildDir = "$buildDir\$vmImgRel"
$vmDeployDir = "$deployRepo\$vmImgRel"
if (-not (Test-Path $vmDeployDir)) { New-Item -ItemType Directory -Path $vmDeployDir -Force | Out-Null }

$programDirs = Get-ChildItem $vmBuildDir -Directory | Sort-Object Name
$batchMaxBytes = 1200MB
$batchNum = 1
$batchSize = 0
$batchDirs = @()

function Push-Batch {
    param($num, $dirs)
    if ($dirs.Count -eq 0) { return }
    Write-Host "  Batch $num`: $($dirs.Count) programs ($($dirs[0])..$($dirs[-1]))" -ForegroundColor Yellow
    Push-Location $deployRepo
    git add "$vmImgRel"
    $st = git status --porcelain
    if ($st) {
        git commit -m "Deploy images batch $num - based on $sourceCommit"
        git push origin $branch
        if ($LASTEXITCODE -ne 0) { Pop-Location; throw "Batch $num push failed." }
    } else {
        Write-Host "    (no changes)" -ForegroundColor DarkGray
    }
    Pop-Location
}

foreach ($d in $programDirs) {
    $dirSize = (Get-ChildItem $d.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum
    if (($batchSize + $dirSize) -gt $batchMaxBytes -and $batchDirs.Count -gt 0) {
        # Push current batch
        Push-Batch -num $batchNum -dirs $batchDirs
        $batchNum++
        $batchSize = 0
        $batchDirs = @()
    }
    # Copy this program dir
    $dest = "$vmDeployDir\$($d.Name)"
    if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
    Copy-Item $d.FullName $dest -Recurse -Force
    $batchSize += $dirSize
    $batchDirs += $d.Name
}

# Push final batch
if ($batchDirs.Count -gt 0) {
    Push-Batch -num $batchNum -dirs $batchDirs
}

Write-Host "`n=== Deploy complete ===" -ForegroundColor Green
