$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest


Get-Content .env | foreach {
    $_ = $_.trim()
    if ($_ -and -not $_.startswith('#') -and $_.contains('=')) {
        $name, $value = $_.split('=', 2)
        $name = $name.trim()
        $value = $value.trim()
        Set-Content env:\$name $value
    }
}