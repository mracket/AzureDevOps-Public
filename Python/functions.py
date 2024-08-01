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
        writer = csv.writer(csvfile, delimiter=';')
        # Write the header row
        writer.writerow(['Id', 'Title', 'AreaPath', 'TeamProject', 'IterationPath', 'WorkItemType', 'State', 'Reason', 'AssignedTo','Parent','CreatedDate','CreatedBy','ChangedDate','ChangedBy','CommentCount','boardColumn','boardColumnDone','description'])

        # Process each work item
        for work_item in work_items:
            work_item_url = work_item['url']
            url = work_item_url + "?$expand=all"
            work_item = requests.get(url, headers=headers).json()
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
                'CommentCount': work_item['fields']['System.CommentCount'],
                'boardColumn': work_item['fields'].get('System.BoardColumn'),
                'boardColumnDone': work_item['fields'].get('System.BoardColumnDone'),
                'description': work_item['fields'].get('System.Description')              
                # Add more fields as needed
            }           

            # Write the work item data to the CSV file
            writer.writerow(work_item_dict.values())

def new_devops_task(devops_org_name,project_id, headers, task_title ,task_description, parent_url):
    if parent_url != None:      
        task_body = [
            {
                "op": "add",
                "path": "/fields/System.Title",
                "value": task_title
            },  
            {
                "op": "add",
                "path": "/relations/-",
                "value": {
                    "rel": "System.LinkTypes.Hierarchy-Reverse",
                    "url": parent_url,
                    "attributes": {
                        "comment": "Making a new task"
                    }
                }                
            },      
            {
                "op": "add",
                "path": "/fields/System.Description",
                "value": task_description
            }
        ]
    else:  
        task_body = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": task_title
        },        
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": task_description
        }
        ]
    url = f"https://dev.azure.com/{devops_org_name}/{project_id}/_apis/wit/workitems/$Task?api-version=7.2-preview.2"
    response = requests.post(url, headers=headers, data=json.dumps(task_body))    
    return response.json()  

def new_devops_userstory(devops_org_name,project_id,headers, userstory_title, userstory_description, parent_url):
    if parent_url != None:      
        userstory_body = [
            {
                "op": "add",
                "path": "/fields/System.Title",
                "value": userstory_title
            },  
            {
                "op": "add",
                "path": "/relations/-",
                "value": {
                    "rel": "System.LinkTypes.Hierarchy-Reverse",
                    "url": parent_url,
                    "attributes": {
                        "comment": "Making a new user story"
                    }
                }                
            },      
            {
                "op": "add",
                "path": "/fields/System.Description",
                "value": userstory_description
            }
        ]
    else:  
        userstory_body = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": userstory_title
        },        
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": userstory_description
        }
        ]
    url = f"https://dev.azure.com/{devops_org_name}/{project_id}/_apis/wit/workitems/$User Story?api-version=7.2-preview.2"
    response = requests.post(url, headers=headers, data=json.dumps(userstory_body))    
    return response.json()

def new_devops_feature(devops_org_name,project_id,headers, feature_title, feature_description, parent_url):
    if parent_url != None:      
        feature_body = [
            {
                "op": "add",
                "path": "/fields/System.Title",
                "value": feature_title
            },  
            {
                "op": "add",
                "path": "/relations/-",
                "value": {
                    "rel": "System.LinkTypes.Hierarchy-Reverse",
                    "url": parent_url,
                    "attributes": {
                        "comment": "Making a new feature"
                    }
                }                
            },      
            {
                "op": "add",
                "path": "/fields/System.Description",
                "value": feature_description
            }
        ]
    else:  
        feature_body = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": feature_title
        },        
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": feature_description
        }
        ]
    url = f"https://dev.azure.com/{devops_org_name}/{project_id}/_apis/wit/workitems/$Feature?api-version=7.2-preview.2"
    response = requests.post(url, headers=headers, data=json.dumps(feature_body))    
    return response.json()

def new_devops_epic(devops_org_name,project_id,headers, epic_title, epic_description=None, epic_area_path=None, epic_assigned_to=None):  
    epic_body = []
    if epic_title is not None:
        epic_body.append({
            "op": "add",
            "path": "/fields/System.Title",
            "value": epic_title
        })

    if epic_description is not None:
        epic_body.append({
            "op": "add",
            "path": "/fields/System.Description",
            "value": epic_description
        })

    if epic_area_path is not None:
        epic_body.append({
            "op": "add",
            "path": "/fields/System.AreaPath",
            "value": epic_area_path
        })
    if epic_assigned_to is not None:
        epic_body.append({
            "op": "add",
            "path": "/fields/System.AssignedTo",
            "value": epic_assigned_to
        })
    url = f"https://dev.azure.com/{devops_org_name}/{project_id}/_apis/wit/workitems/$Epic?api-version=7.2-preview.2"
    response = requests.post(url, headers=headers, data=json.dumps(epic_body))    
    return response.json()

def update_devops_epic(devops_org_name,project_id,headers, epic_id, epic_state=None, epic_title=None, epic_description=None, epic_area_path=None, epic_assigned_to=None):   
    epic_body = []   
    if epic_title is not None:
        epic_body.append({
            "op": "add",
            "path": "/fields/System.Title",
            "value": epic_title
        })

    if epic_description is not None:
        epic_body.append({
            "op": "add",
            "path": "/fields/System.Description",
            "value": epic_description
        })

    if epic_area_path is not None:
        epic_body.append({
            "op": "add",
            "path": "/fields/System.AreaPath",
            "value": epic_area_path
        })
    if epic_assigned_to is not None:
        epic_body.append({
            "op": "add",
            "path": "/fields/System.AssignedTo",
            "value": epic_assigned_to
        })  
    if epic_state is not None:
        epic_body.append({
            "op": "add",
            "path": "/fields/System.State",
            "value": epic_state
        })
    url = f"https://dev.azure.com/{devops_org_name}/{project_id}/_apis/wit/workitems/{epic_id}?api-version=7.2-preview.3"
    response = requests.patch(url, headers=headers, data=json.dumps(epic_body))    
    return response.json()

def import_devops_workitems(devops_org_name,project_id,headers, file_name):
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Each row is a list of strings
            # Process each row as needed
            print(row)