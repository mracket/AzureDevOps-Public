function Get-DevOpsProjectTeams {
    param (
        [string]$DevOpsOrgName,
        [hashtable]$Headers,
        [string]$ProjectId
    )
    $Result = Invoke-RestMethod -Uri "https://dev.azure.com/$DevOpsOrgName/_apis/projects/$ProjectId/teams?api-version=7.2-preview.3" -Method GET -Headers $Headers -ContentType "application/json-patch+json"
    Return  $Result.value
}

