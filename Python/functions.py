import requests
import json
import csv

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

def write_to_csv(work_items, output_file_name, headers): 
    with open(output_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header row
        writer.writerow(['Id', 'Title', 'AreaPath', 'TeamProject', 'IterationPath', 'WorkItemType', 'State', 'Reason', 'AssignedTo','Parent','CreatedDate','CreatedBy','ChangedDate','ChangedBy','CommentCount','boardColumn','boardColumnDone','description'])

        # Process each work item
        for work_item in work_items:
            work_item_url = work_item['url']
            url = work_item_url + "?$expand=all"
            work_item = requests.get(url, headers=headers).json()
            print(work_item)
            work_item_dict = {                
                'Id': work_item['id'],
                'Title': work_item['fields']['System.Title'],
                'AreaPath': work_item['fields']['System.AreaPath'],
                'TeamProject': work_item['fields']['System.TeamProject'],
                'IterationPath': work_item['fields']['System.IterationPath'],
                'WorkItemType': work_item['fields']['System.WorkItemType'],
                'State': work_item['fields']['System.State'],
                'Reason': work_item['fields']['System.Reason'],
                'AssignedTo': work_item['fields'].get('System.AssignedTo'),
                'Parent': work_item['fields'].get('System.Parent'),
                'CreatedDate': work_item['fields']['System.CreatedDate'],
                'CreatedBy': work_item['fields']['System.CreatedBy'],
                'ChangedDate': work_item['fields']['System.ChangedDate'],
                'ChangedBy': work_item['fields']['System.ChangedBy'],
                'CommentCount': work_item['fields']['System.CommentCount'],
                'description': work_item['fields'].get('System.Description')              
                # Add more fields as needed
            }           

            # Write the work item data to the CSV file
            writer.writerow(work_item_dict.values())