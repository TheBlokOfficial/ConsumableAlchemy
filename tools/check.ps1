# Fast pre-game gate: run before deploy.ps1.
#   powershell -ExecutionPolicy Bypass -File tools/check.ps1
# Checks: generated recipe table is up to date, .ws lint (wrappedMethod once, vars first),
# recipe rule errors (validate.py), no game data tracked or staged in git. Prints CHECK OK / CHECK FAILED (n), exit 0 / 1.

$Root = Split-Path -Parent $PSScriptRoot
$failed = 0

Write-Host "== Generated recipe table =="
& python (Join-Path $Root "tools\recipes\generate.py") --check
if ($LASTEXITCODE -ne 0) { $failed++ }

Write-Host ""
Write-Host "== WitcherScript lint =="
& python (Join-Path $Root "tools\lint_ws.py") (Join-Path $Root "src")
if ($LASTEXITCODE -ne 0) { $failed++ }

Write-Host ""
Write-Host "== Recipe rules (errors only) =="
& python (Join-Path $Root "tools\recipes\validate.py") --errors-only
if ($LASTEXITCODE -ne 0) { $failed++ }

Write-Host ""
Write-Host "== Game data not in git =="
$guarded = @("tools/recipes/x/", "tools/recipes/data.json")
$tracked = @(& git -C $Root ls-files -- $guarded)
$staged = @(& git -C $Root diff --cached --name-only -- $guarded)
$bad = @($tracked + $staged | Where-Object { $_ } | Sort-Object -Unique)
if ($bad.Count -gt 0) {
    foreach ($b in $bad) { Write-Host "tracked or staged: $b" }
    $failed++
} else {
    Write-Host "ok"
}

Write-Host ""
if ($failed -eq 0) {
    Write-Host "CHECK OK"
    exit 0
}
Write-Host "CHECK FAILED ($failed)"
exit 1
