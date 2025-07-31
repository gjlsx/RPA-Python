param(
    [Parameter(Position=0)]
    [int]$StartNum,
    
    [Parameter(Position=1)]
    [int]$Count
)

# Change to script directory
Set-Location $PSScriptRoot

Write-Host "Chrome Shortcut Generator" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green

# Check if parameters are provided
if (-not $StartNum -or -not $Count) {
    Write-Host "Usage: .\genchrome.ps1 <start_number> <count>" -ForegroundColor Yellow
    Write-Host "Example: .\genchrome.ps1 11 10" -ForegroundColor Yellow
    Write-Host ""
    
    # Interactive mode
    do {
        $StartNum = Read-Host "Enter start number"
    } while (-not $StartNum -or $StartNum -notmatch '^\d+$')
    
    do {
        $Count = Read-Host "Enter count"
    } while (-not $Count -or $Count -notmatch '^\d+$')
}

Write-Host ""
Write-Host "Starting number: $StartNum" -ForegroundColor Cyan
Write-Host "Count: $Count" -ForegroundColor Cyan
Write-Host ""

# Run Python script
try {
    python chrome_shortcut_generator.py $StartNum $Count
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Success!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "Error occurred!" -ForegroundColor Red
    }
} catch {
    Write-Host "Error running Python script: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
