$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest


try {


    Write-Host "=== Nephila MS Messenger ===`n"


    .\scripts\helpers\_load_envs.ps1


    if ($args -contains "docker") {

        .\scripts\helpers\_stop.ps1 docker
        Write-Host "Starting Nephila MS Messenger..."

        $logs_dir = ".\logs"
        if (-not (Test-Path $logs_dir)) {
            New-Item -ItemType Directory $logs_dir | Out-Null
        }

        docker build -f Dockerfile.w -t ${Env:APP_NAME} .
        docker run `
            --publish 127.0.0.1:${Env:PORT}:${Env:PORT} `
            --env-file .env `
            --env RUN_MODE=docker `
            --name ${Env:APP_NAME} `
            --mount type=bind,src="${PWD}"/logs,target=/usr/src/logs `
            --detach `
            ${Env:APP_NAME}

    }

    else {

        .\scripts\helpers\_stop.ps1
        Write-Host "Starting Nephila MS Messenger..."

        .\env\Scripts\Activate.ps1
        python waitress.serve.py

    }


}


finally {

    if ($args -contains "debug") {
        Read-Host "`n=== ENTER to exit ==="
    }

}