import requests
import json

def get_devops_projects(devops_org_name, headers):
    url = f"https://dev.azure.com/{devops_org_name}/_apis/projects?api-version=7.2-preview.4"
    response = requests.get(url, headers=headers)
    return response.json()['value']

def get_devops_project_teams(devops_org_name, project_id, headers):
    url = f"https://dev.azure.com/{devops_org_name}/_apis/projects/{project_id}/teams?api-version=7.2-preview.3"
    response = requests.get(url, headers=headers)
    return response.json()['value']

def get_devops_project_team_tasks(devops_org_name, project_id, team,headers):
    url = f"https://dev.azure.com/{devops_org_name}/{project_id}/{team}/_apis/wit/wiql?api-version=7.2-preview.2"
    task_body = {
        "query": "Select [System.Id], [System.Title], [System.State], [System.TeamProject],[System.Parent] From WorkItems order by [Microsoft.VSTS.Common.Priority] asc, [System.CreatedDate] desc"
    }    
    response = requests.post(url, headers=headers,json=task_body)
    return response.json()['workItems']

def get_devops_task(url, headers):
    response = requests.get(url, headers=headers)
    return response.json()


