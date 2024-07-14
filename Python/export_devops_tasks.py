import requests
import base64
import json
import functions as f
import csv
import argparse

# Parameters
# Create the parser
parser = argparse.ArgumentParser(description="Export Azure DevOps tasks to a CSV file.")

# Add the arguments
parser.add_argument('--PAT', type=str, help="The Personal Access Token.")
parser.add_argument('--devops_org_name', type=str, help="The name of the Azure DevOps organization.")
parser.add_argument('--output_file_name', type=str, help="The name of the output CSV file.")

# Parse the arguments
args = parser.parse_args()

# Prepare the headers with the PAT
token = base64.b64encode(bytes(':' + args.PAT, 'ascii')).decode('ascii')
headers = {'Authorization': 'Basic ' + token}

# Get the projects, teams, and work items
projects = f.get_devops_projects(args.devops_org_name, headers)
teams = f.get_devops_project_teams(args.devops_org_name, projects[0]['id'], headers)
work_items = f.get_devops_project_team_tasks(args.devops_org_name, projects[0]['id'], teams[0]['id'], headers)

with open(args.output_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header row
        writer.writerow(['Id', 'Title', 'AreaPath', 'TeamProject', 'IterationPath', 'WorkItemType', 'State', 'Reason', 'AssignedTo','Parent'])

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
                'Parent': work_item['fields'].get('System.Parent')
                # Add more fields as needed
            }
            

            # Write the work item data to the CSV file
            writer.writerow(work_item_dict.values())