#!/usr/bin/env pwsh
# Convert ingest program guides to Docusaurus format
# Preserves existing frontmatter, converts image paths to existing static assets

$docsDir = "c:\Users\lars\lzxtm\docs\instruments\videomancer\programs"
$ingestDir = "c:\Users\lars\lzxtm\ingest\videomancer\docs\programs"

# Dynamically find all programs that have both a doc file and an ingest guide
$programs = Get-ChildItem $ingestDir -Directory |
    Where-Object { Test-Path (Join-Path $_.FullName "$($_.Name)_program_guide.md") } |
    Where-Object { Test-Path (Join-Path $docsDir "$($_.Name).md") } |
    ForEach-Object { $_.Name } |
    Sort-Object

foreach ($prog in $programs) {
    $existingFile = Join-Path $docsDir "$prog.md"
    $ingestFile = Join-Path $ingestDir "$prog\${prog}_program_guide.md"
    
    if (-not (Test-Path $existingFile)) {
        Write-Warning "Existing file not found: $existingFile"
        continue
    }
    if (-not (Test-Path $ingestFile)) {
        Write-Warning "Ingest file not found: $ingestFile"
        continue
    }
    
    # Extract frontmatter from existing file
    $existingContent = Get-Content $existingFile -Raw -Encoding UTF8
    if ($existingContent -match '(?s)^(---\s*\n.*?\n---)\s*\n') {
        $frontmatter = $Matches[1]
    } else {
        Write-Warning "No frontmatter found in: $existingFile"
        continue
    }
    
    # Read ingest content
    $ingestContent = Get-Content $ingestFile -Raw -Encoding UTF8
    
    # Remove DO NOT EDIT comments at the top
    $ingestContent = $ingestContent -replace '(?s)^<!--.*?-->\s*\n', ''
    # May be multiple comment blocks
    $ingestContent = $ingestContent -replace '(?s)^<!--.*?-->\s*\n', ''
    
    # Remove the title line "# XYZ — Program Guide" (em-dash may vary in encoding)
    $ingestContent = $ingestContent -replace '(?m)^# .+Program Guide\s*\n', ''
    $ingestContent = $ingestContent -replace '(?m)^> \*\*Categories\*\*:.*\n', ''
    $ingestContent = $ingestContent -replace '(?m)^> \*\*Type\*\*:.*\n', ''
    $ingestContent = $ingestContent -replace '(?m)^> \*\*Version\*\*:.*\n', ''
    $ingestContent = $ingestContent -replace '(?m)^> \*\*Author\*\*:.*\n', ''
    $ingestContent = $ingestContent -replace '(?m)^> \*\*Core\*\*:.*\n', ''
    
    # Remove "Related Programs" section at the end
    $ingestContent = $ingestContent -replace '(?s)\n## Related Programs\b.*$', ''
    
    # Remove closing line about Videomancer program library
    $ingestContent = $ingestContent -replace '(?m)^\*.*part of the Videomancer program library.*\*\s*$', ''
    
    # Convert image paths: assets/{prog}_X.png -> /img/instruments/videomancer/{prog}/{prog}_X.png
    # But map specific filenames that don't exist:
    #   {prog}_hero.png -> {prog}_hero_s1.png
    #   {prog}_exercise1_result.png -> {prog}_ex1_s1.png
    #   {prog}_exercise2_result.png -> {prog}_ex2_s1.png
    #   {prog}_exercise3_result.png -> {prog}_ex3_s1.png
    
    $imgBase = "/img/instruments/videomancer/$prog"
    
    # First, handle specific mappings
    $ingestContent = $ingestContent -replace [regex]::Escape("assets/${prog}_hero.png"), "$imgBase/${prog}_hero_s1.png"
    $ingestContent = $ingestContent -replace [regex]::Escape("assets/${prog}_exercise1_result.png"), "$imgBase/${prog}_ex1_s1.png"
    $ingestContent = $ingestContent -replace [regex]::Escape("assets/${prog}_exercise2_result.png"), "$imgBase/${prog}_ex2_s1.png"
    $ingestContent = $ingestContent -replace [regex]::Escape("assets/${prog}_exercise3_result.png"), "$imgBase/${prog}_ex3_s1.png"
    
    # Then handle remaining assets/ references (control_panel, etc.)
    $ingestContent = $ingestContent -replace "assets/($prog)", "$imgBase/`$1"
    # Catch any remaining assets/ references for this program
    $ingestContent = $ingestContent -replace "assets/", "$imgBase/"
    
    # Clean up leading whitespace/newlines
    $ingestContent = $ingestContent.TrimStart()
    
    # Remove leading --- separator left from metadata block removal
    $ingestContent = $ingestContent -replace '(?s)^---\s*\n', ''
    $ingestContent = $ingestContent.TrimStart()
    
    # Collapse consecutive --- separators (with blank lines between) into single ---
    $ingestContent = $ingestContent -replace '(?m)^---\s*\n(\s*\n)+---\s*$', '---'
    
    # Remove trailing whitespace
    $ingestContent = $ingestContent.TrimEnd()
    
    # Combine frontmatter + new content
    $result = "$frontmatter`n`n$ingestContent`n"
    
    # Write result
    Set-Content -Path $existingFile -Value $result -Encoding UTF8 -NoNewline
    
    Write-Output "Updated: $prog"
}

Write-Output "`nDone! Updated $($programs.Count) program guides."
