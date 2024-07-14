param (
    [string]$PAT,
    [string]$DevOpsOrgName,
    [string]$OutputFileName
)


Import-Module $PSScriptRoot\..\Modules\CloudninjaDevOps\CloudninjaDevOps.psm1 -Force
$Token = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes(":$($PAT)"))
$Headers = @{authorization = "Basic $Token"}

$Projects = Get-DevOpsProjects -DevOpsOrgName "$DevOpsOrgName" -Headers $Headers # | ConvertFrom-Json -Depth 10
$Teams = Get-DevOpsProjectTeams -DevOpsOrgName "$DevOpsOrgName" -ProjectID $($Projects[0].id) -Headers $Headers
$WorkItems = Get-DevOpsProjectTeamTasks -DevOpsOrgName "$DevOpsOrgName" -ProjectID $($Projects[0].id) -Team $($Teams[0].id) -Headers $Headers

$objectCollection=@()

foreach($WorkItemURL in $($WorkItems.WorkITems.url)) {
    $URL = "$WorkItemURL`?`$expand=all"
    $WorkItem = (Get-DevOpsTask -URL $URL -Headers $Headers).Content | ConvertFrom-Json -Depth 10
    $object = New-Object PSObject
    Add-Member -InputObject $object -MemberType NoteProperty -Name Id -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name Title -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name AreaPath -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name TeamProject -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name IterationPath -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name WorkItemType -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name State -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name Reason -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name AssignedTo -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name CreatedDate -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name CreatedBy -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name ChangedDate -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name ChangedBy -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name CommentCount -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name BoardColumn -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name BoardColumnDone -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name Description -Value ""
    Add-Member -InputObject $object -MemberType NoteProperty -Name Parent -Value ""

    $object.Id = $WorkItem.Id
    $object.Title = $WorkItem.Fields.'System.Title'
    $object.AreaPath = $WorkItem.Fields.'System.AreaPath'
    $object.TeamProject = $WorkItem.Fields.'System.TeamProject'
    $object.IterationPath = $WorkItem.Fields.'System.IterationPath'
    $object.WorkItemType = $WorkItem.Fields.'System.WorkItemType'
    $object.State = $WorkItem.Fields.'System.State'
    $object.Reason = $WorkItem.Fields.'System.Reason'
    $object.AssignedTo = $WorkItem.Fields.'System.AssignedTo'
    $object.CreatedDate = $WorkItem.Fields.'System.CreatedDate'
    $object.CreatedBy = $WorkItem.Fields.'System.CreatedBy'
    $object.ChangedDate = $WorkItem.Fields.'System.ChangedDate'
    $object.ChangedBy = $WorkItem.Fields.'System.ChangedBy'
    $object.CommentCount = $WorkItem.Fields.'System.CommentCount'
    $object.BoardColumn = $WorkItem.Fields.'System.BoardColumn'
    $object.BoardColumnDone = $WorkItem.Fields.'System.BoardColumnDone'
    $object.Description = $WorkItem.Fields.'System.Description'
    $object.Parent = $WorkItem.Fields.'System.Parent'
    $objectCollection += $object

}
$objectCollection | Export-Csv -Path $PSScriptRoot\$OutputFileName -NoTypeInformation -Delimiter ";" -Encoding UTF8
