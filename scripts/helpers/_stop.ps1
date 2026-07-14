$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest


try {


    Write-Host "Stopping Nephila MS Messenger..."


    .\scripts\helpers\_load_envs.ps1


    if ($args -contains "docker") {

        docker stop ${Env:APP_NAME}
        docker rm ${Env:APP_NAME}
        docker rmi ${Env:APP_NAME}
    }

    else {

        $pid_file = ".\.pid"

        if (Test-Path $pid_file) {
            Stop-Process -Id (Get-Content $pid_file)
            Remove-Item -Path $pid_file
        }

    }


    Write-Host "Nephila MS Messenger has stopped."


}


finally {

    if ($args -contains "debug") {
        Read-Host "`n=== ENTER to exit ==="
    }

}