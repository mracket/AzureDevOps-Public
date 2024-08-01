import base64
import functions as f
import argparse
import csv
import json

# Parameters
# Create the parser
parser = argparse.ArgumentParser(description="Create new devops task")

# Add the arguments
parser.add_argument('--PAT', type=str, help="The Personal Access Token.")
parser.add_argument('--devops_org_name', type=str, help="The name of the Azure DevOps organization.")
parser.add_argument('--project_name', type=str, help="The name of the project.")
parser.add_argument('--name', type=str, help="The name of the task.")
parser.add_argument('--description', type=str, help="The description of the task.")
parser.add_argument('--type', type=str, help="The type of the task.")
parser.add_argument('--parent_url', type=str, help="The parent task URL.")
parser.add_argument('--file', type=str, help="The file to import the work items from.")

# Parse the arguments
args = parser.parse_args()

# Prepare the headers with the PAT
token = base64.b64encode(bytes(':' + args.PAT, 'ascii')).decode('ascii')
headers = {'Authorization': 'Basic ' + token, 'Content-Type': 'application/json-patch+json'}

# Create DevOps epic
if args.type == "epic":
    result = f.new_devops_epic(args.devops_org_name, args.project_name,headers, args.name, args.description)

# Create DevOps feature
if args.type == "feature" and args.parent_url == None:
    result = f.new_devops_feature(args.devops_org_name, args.project_name,headers, args.name, args.description, None)
elif args.type == "feature":
    result = f.new_devops_feature(args.devops_org_name, args.project_name,headers, args.name, args.description, args.parent_url)

# Create DevOps user story
if args.type == "user_story" and args.parent_url == None:
    result = f.new_devops_userstory(args.devops_org_name, args.project_name,headers, args.name, args.description, None)
elif args.type == "user_story":
    result = f.new_devops_userstory(args.devops_org_name, args.project_name,headers, args.name, args.description, args.parent_url)

# Create new DevOps Task
if args.type == "task" and args.parent_url == None:
    result = f.new_devops_task(args.devops_org_name, args.project_name,headers, args.name, args.description, None)
elif args.type == "task":
    result = f.new_devops_task(args.devops_org_name, args.project_name,headers, args.name, args.description, args.parent_url)

if args.type == "import":
    with open(args.file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:   
            try:
                id = row['Id']
                url = f"https://dev.azure.com/{args.devops_org_name}/{args.project_name}/_apis/wit/workitems/{id}?api-version=7.2-preview.3"
                work_item = f.get_devops_task(url, headers)
                if 'errorCode' in work_item:
                    raise Exception('No work items found')             
                print("Work items found, skipping import")
            except: 
                print("No work items found, importing new ones")
                if(row['WorkItemType'] == "Epic"):    
                    if row['AssignedTo'] and row['AssignedTo'].strip() != 'None':
                        assigned_to_json = row['AssignedTo'].replace("'", '"')
                        assigned_to = json.loads(assigned_to_json)
                    result = f.new_devops_epic(args.devops_org_name, args.project_name, headers,row['Id'], row['Title'], row['description'], row['AreaPath'],assigned_to['uniqueName'])
                    if(row['State'] != "New"):
                        result1 = f.update_devops_epic(args.devops_org_name, args.project_name, headers,result['id'], row['State'])

# print(result)   


