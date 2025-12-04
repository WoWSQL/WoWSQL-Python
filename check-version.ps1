# Script to check and verify version consistency across all files
# Run this before publishing to ensure all versions match

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Version Consistency Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check pyproject.toml (source of truth)
$pyprojectVersion = $null
if (Test-Path "pyproject.toml") {
    $pyprojectMatch = Select-String -Path "pyproject.toml" -Pattern 'version\s*=\s*"([^"]+)"'
    if ($pyprojectMatch) {
        $pyprojectVersion = $pyprojectMatch.Matches.Groups[1].Value
    }
}

# Check __init__.py
$initVersion = $null
$initPath = "src\wowsql\__init__.py"
if (Test-Path $initPath) {
    $initMatch = Select-String -Path $initPath -Pattern '__version__\s*=\s*"([^"]+)"'
    if ($initMatch) {
        $initVersion = $initMatch.Matches.Groups[1].Value
    }
}

# Check setup.py
$setupVersion = $null
if (Test-Path "setup.py") {
    $setupMatch = Select-String -Path "setup.py" -Pattern 'version\s*=\s*"([^"]+)"'
    if ($setupMatch) {
        $setupVersion = $setupMatch.Matches.Groups[1].Value
    }
}

# Display results
Write-Host "Version in pyproject.toml: " -NoNewline
if ($pyprojectVersion) {
    Write-Host "$pyprojectVersion" -ForegroundColor Green
} else {
    Write-Host "NOT FOUND" -ForegroundColor Red
}

Write-Host "Version in __init__.py:    " -NoNewline
if ($initVersion) {
    if ($initVersion -eq $pyprojectVersion) {
        Write-Host "$initVersion [OK]" -ForegroundColor Green
    } else {
        Write-Host "$initVersion [MISMATCH]" -ForegroundColor Red
    }
} else {
    Write-Host "NOT FOUND" -ForegroundColor Yellow
}

Write-Host "Version in setup.py:       " -NoNewline
if ($setupVersion) {
    if ($setupVersion -eq $pyprojectVersion) {
        Write-Host "$setupVersion [OK]" -ForegroundColor Green
    } else {
        Write-Host "$setupVersion [MISMATCH]" -ForegroundColor Red
    }
} else {
    Write-Host "NOT FOUND (optional)" -ForegroundColor Gray
}

Write-Host ""

# Check dist folder
Write-Host "Built distributions:" -ForegroundColor Cyan
$distFiles = Get-ChildItem -Path "dist" -Filter "*.whl" -ErrorAction SilentlyContinue
if ($distFiles) {
    foreach ($file in $distFiles) {
        if ($file.Name -match 'wowsql-([\d.]+)') {
            $distVersion = $matches[1]
            Write-Host "  $($file.Name)" -ForegroundColor $(if ($distVersion -eq $pyprojectVersion) { "Green" } else { "Yellow" })
        }
    }
} else {
    Write-Host "  No distributions found in dist/ folder" -ForegroundColor Yellow
}

Write-Host ""

# Summary
if ($pyprojectVersion) {
    if (($initVersion -eq $pyprojectVersion) -and ($setupVersion -eq $pyprojectVersion -or -not $setupVersion)) {
        Write-Host "✅ All versions are synchronized!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Current version: $pyprojectVersion" -ForegroundColor Cyan
        Write-Host "Ready to publish!" -ForegroundColor Green
    } else {
        Write-Host "❌ Version mismatch detected!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Action required:" -ForegroundColor Yellow
        Write-Host "  1. Update all files to match pyproject.toml version: $pyprojectVersion" -ForegroundColor White
        Write-Host "  2. Run this script again to verify" -ForegroundColor White
        exit 1
    }
} else {
    Write-Host "❌ Could not find version in pyproject.toml" -ForegroundColor Red
    exit 1
}

Write-Host ""

