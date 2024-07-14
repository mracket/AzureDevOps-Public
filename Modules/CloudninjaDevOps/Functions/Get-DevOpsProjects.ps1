function Get-DevOpsProjects {
    param (
        [string]$DevOpsOrgName,
        [hashtable]$Headers
    )
    $Result = Invoke-RestMethod -Uri "https://dev.azure.com/$DevOpsOrgName/_apis/projects?api-version=7.2-preview.4" -Method GET -Headers $Headers -ContentType "application/json-patch+json"
    Return  $Result.Value
}



