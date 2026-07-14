$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest


Push-Location (Split-Path (Split-Path $MyInvocation.MyCommand.Path -Parent) -Parent)


try {

    if ($args -contains "docker") {
        Write-Host "-- Stop MS Messenger from Docker --"
    }

    else {
        Write-Host "-- Stop MS Messenger process --"
    }

    Start-Process -FilePath "powershell.exe" -ArgumentList (@("-File", ".\scripts\helpers\_stop.ps1") + $args)

}


finally {
    Pop-Location
}