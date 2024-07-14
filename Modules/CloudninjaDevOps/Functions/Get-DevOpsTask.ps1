function Get-DevOpsTask {
    param (
        [string]$URL,
        [hashtable]$Headers
    )
    $Result = Invoke-WebRequest -Uri $URL -Headers $headers -ContentType "application/json" -UseBasicParsing
    Return  $Result
}
