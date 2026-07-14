$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest


Push-Location (Split-Path (Split-Path $MyInvocation.MyCommand.Path -Parent) -Parent)


try {

    if ($args -contains "docker") {
        Write-Host "-- Start MS Messenger with Docker --"
    }

    else {
        Write-Host "-- Start MS Messenger process --"
    }

    Start-Process -FilePath "powershell.exe" -ArgumentList (@("-File", ".\scripts\helpers\_start.ps1") + $args)

}


finally {
    Pop-Location
}