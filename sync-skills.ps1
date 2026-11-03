<#
.SYNOPSIS
    Synchronizes and updates cloned skills from external repositories while preserving local skills and protected files.
.PARAMETER DryRun
    Simulates the update and displays which files would be added or modified without changing local files.
.PARAMETER SkillName
    Filters the update to a single skill name (e.g., -SkillName supabase).
.PARAMETER ForceProtected
    Overwrites files listed in protectedFiles if specified.
#>
param(
    [switch]$DryRun,
    [string]$SkillName = "",
    [switch]$ForceProtected
)

$ErrorActionPreference = "Stop"
$SkillsRoot = $PSScriptRoot
$ManifestPath = Join-Path $SkillsRoot "skills-manifest.json"

if (-not (Test-Path $ManifestPath)) {
    Write-Error "Manifest not found at: $ManifestPath"
    exit 1
}

$manifest = Get-Content -Path $ManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$skillsToProcess = $manifest.skills

if ($SkillName) {
    $skillsToProcess = $skillsToProcess | Where-Object { $_.name -eq $SkillName }
    if (-not $skillsToProcess) {
        Write-Warning "No skill found in manifest with name '$SkillName'."
        exit 0
    }
}

$tempBase = Join-Path $env:TEMP ("codex-skills-sync-" + [guid]::NewGuid().ToString("N").Substring(0, 8))
New-Item -ItemType Directory -Path $tempBase -Force | Out-Null

try {
    $remoteSkills = $skillsToProcess | Where-Object { $_.mode -eq "overlay" -and $_.repo }
    $repoGroups = $remoteSkills | Group-Object { "$($_.repo)|$($_.branch)" }

    $clonedRepos = @{}

    foreach ($group in $repoGroups) {
        $parts = $group.Name -split "\|"
        $repoUrl = $parts[0]
        $branch = $parts[1]
        $repoSlug = ($repoUrl -replace "https://github.com/", "" -replace "\.git$", "" -replace "/", "_")
        $cloneDir = Join-Path $tempBase $repoSlug

        Write-Host "`n[Clone] Fetching $repoUrl ($branch)..." -ForegroundColor Cyan
        git clone --depth 1 --branch $branch --single-branch $repoUrl $cloneDir --quiet
        $clonedRepos[$group.Name] = $cloneDir
    }

    Write-Host "`n================ SYNC REPORT ================" -ForegroundColor White

    foreach ($skill in $skillsToProcess) {
        $name = $skill.name
        $mode = $skill.mode
        $targetDir = Join-Path $SkillsRoot $name

        if ($mode -eq "local") {
            Write-Host "[$name] " -NoNewline -ForegroundColor Blue
            Write-Host "SKIP (Local / Authorial skill)" -ForegroundColor Gray
            continue
        }

        if ($mode -eq "pinned") {
            Write-Host "[$name] " -NoNewline -ForegroundColor Yellow
            Write-Host "PINNED ($($skill.notes))" -ForegroundColor DarkYellow
            continue
        }

        $key = "$($skill.repo)|$($skill.branch)"
        $cloneDir = $clonedRepos[$key]
        $sourceDir = if ($skill.subPath) { Join-Path $cloneDir ($skill.subPath -replace "/", "\") } else { $cloneDir }

        if (-not (Test-Path $sourceDir)) {
            Write-Host "[$name] ERROR: Subpath '$($skill.subPath)' not found in $($skill.repo)" -ForegroundColor Red
            continue
        }

        $protected = @()
        if ($skill.protectedFiles) { $protected = @($skill.protectedFiles) }

        $excludes = @(".git", ".git/*", ".github", ".github/*")
        if ($skill.excludeFiles) { $excludes += @($skill.excludeFiles) }

        $sourceFiles = Get-ChildItem -Path $sourceDir -Recurse -File -Force | Where-Object {
            $rel = $_.FullName.Substring($sourceDir.Length + 1).Replace("\", "/")
            $skip = $false
            foreach ($pattern in $excludes) {
                if ($rel -like $pattern) { $skip = $true; break }
            }
            -not $skip
        }

        $added = @()
        $updated = @()
        $skippedProtected = @()

        foreach ($sf in $sourceFiles) {
            $relPath = $sf.FullName.Substring($sourceDir.Length + 1).Replace("\", "/")
            $destFile = Join-Path $targetDir ($relPath.Replace("/", "\"))

            if (($relPath -in $protected) -and (-not $ForceProtected) -and (Test-Path $destFile)) {
                $skippedProtected += $relPath
                continue
            }

            if (-not (Test-Path $destFile)) {
                $added += $relPath
                if (-not $DryRun) {
                    $destParent = Split-Path $destFile -Parent
                    if (-not (Test-Path $destParent)) {
                        New-Item -ItemType Directory -Path $destParent -Force | Out-Null
                    }
                    Copy-Item -Path $sf.FullName -Destination $destFile -Force
                }
            } else {
                $srcBytes = [System.IO.File]::ReadAllBytes($sf.FullName)
                $dstBytes = [System.IO.File]::ReadAllBytes($destFile)
                $isSame = $false

                if ($srcBytes.Length -eq $dstBytes.Length) {
                    $srcHash = [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($srcBytes))
                    $dstHash = [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($dstBytes))
                    $isSame = ($srcHash -eq $dstHash)
                }

                if (-not $isSame) {
                    try {
                        $srcText = ([System.IO.File]::ReadAllText($sf.FullName)).Replace("`r`n", "`n")
                        $dstText = ([System.IO.File]::ReadAllText($destFile)).Replace("`r`n", "`n")
                        $isSame = ($srcText -eq $dstText)
                    } catch {
                        $isSame = $false
                    }
                }

                if (-not $isSame) {
                    $updated += $relPath
                    if (-not $DryRun) {
                        Copy-Item -Path $sf.FullName -Destination $destFile -Force
                    }
                }
            }
        }

        Write-Host "[$name] " -NoNewline -ForegroundColor Cyan
        if ($added.Count -eq 0 -and $updated.Count -eq 0) {
            Write-Host "Up to date (0 changes)" -ForegroundColor Green -NoNewline
        } else {
            $prefix = if ($DryRun) { "[DRY-RUN] " } else { "" }
            Write-Host "$($prefix)+$($added.Count) new, ~$($updated.Count) updated" -ForegroundColor Yellow -NoNewline
        }
        if ($skippedProtected.Count -gt 0) {
            Write-Host " (Protected kept: $($skippedProtected -join ', '))" -ForegroundColor DarkGray
        } else {
            Write-Host ""
        }

        foreach ($a in $added) { Write-Host "    + $a" -ForegroundColor Green }
        foreach ($u in $updated) { Write-Host "    ~ $u" -ForegroundColor Yellow }
    }

    Write-Host "`nDone! Run 'git status' and 'git diff' in $SkillsRoot to review changes." -ForegroundColor Green
} finally {
    if (Test-Path $tempBase) {
        Remove-Item -Path $tempBase -Recurse -Force -ErrorAction SilentlyContinue
    }
}
