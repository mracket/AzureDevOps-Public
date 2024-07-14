import base64
import functions as f
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

f.write_to_csv(work_items, args.output_file_name, headers)