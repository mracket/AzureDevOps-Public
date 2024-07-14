function Get-DevOpsProjectTeamTasks {
    param (
        [string]$DevOpsOrgName,
        [hashtable]$Headers,
        [string]$ProjectId,
        [string]$Team
    )
$TaskBody = 
@"    
{
    "query": "Select [System.Id], [System.Title], [System.State], [System.TeamProject],[System.Parent] From WorkItems order by [Microsoft.VSTS.Common.Priority] asc, [System.CreatedDate] desc"
}      
"@         
    $Result = Invoke-RestMethod -Uri "https://dev.azure.com/$DevOpsOrgName/$ProjectId/$Team/_apis/wit/wiql?api-version=7.2-preview.2" -Body $TaskBody -Method POST -Headers $Headers -ContentType "application/json"
    Return  $Result
}


