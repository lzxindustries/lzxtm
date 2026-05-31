#!/usr/bin/env pwsh
# Deploy script for docs.lzxindustries.net redirect site.
# Pushes the 4-file redirect-site/ directory to GitHub Pages.
# No build step required.

$ErrorActionPreference = 'Stop'

$root        = $PSScriptRoot
$redirectDir = Join-Path $root "redirect-site"
$deployRepo  = Join-Path $root ".deploy-repo"
$repoUrl     = "https://github.com/lzxindustries/lzxindustries.github.io.git"
$branch      = "main"

# 1. Ensure persistent deploy repo clone exists
if (Test-Path (Join-Path $deployRepo ".git")) {
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

# 2. Clear all tracked content from deploy repo
Write-Host "`n=== Clearing deploy repo content ===" -ForegroundColor Cyan
Push-Location $deployRepo
Get-ChildItem -Force | Where-Object { $_.Name -ne '.git' } | Remove-Item -Recurse -Force
Pop-Location

# 3. Copy redirect-site files (including hidden .nojekyll)
Write-Host "`n=== Copying redirect-site files ===" -ForegroundColor Cyan
Get-ChildItem -Path $redirectDir -Force | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination (Join-Path $deployRepo $_.Name) -Force
}

# 4. Commit and push
$sourceCommit = (git -C $root rev-parse --short HEAD)
Push-Location $deployRepo
git add --all
$status = git status --porcelain
if ($status) {
    git commit -m "Deploy redirect site - based on $sourceCommit"
    Write-Host "`n=== Pushing ===" -ForegroundColor Cyan
    git push origin $branch
    if ($LASTEXITCODE -ne 0) { Pop-Location; throw "Push failed." }
    Write-Host "`n=== Done ===" -ForegroundColor Green
} else {
    Write-Host "No changes to deploy." -ForegroundColor Yellow
}
Pop-Location
