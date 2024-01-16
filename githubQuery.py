####################################################################################
#                                                                                  #
# Author: Aldo Mestas                                                              #
# Application to interact with Github API and obtain ummary of all opened, closed, #
# and in progress pull requests in the last week for a given repository and print  #
# an email summary report that might be sent to a manager or Scrum-master.         #
#                                                                                  #
# January 2024                                                                     #
#                                                                                  #
####################################################################################


import requests
from datetime import datetime, timedelta

# Function which queries github for pull requests 

def get_pull_requests_details(owner, repo, token):
    base_url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    headers = {'Authorization': f'token {token}'}
    
    # Calculate the date one week ago
    one_week_ago = (datetime.now() - timedelta(weeks=1)).isoformat()

    # Define parameters for the GitHub API request
    params = {
        'state': 'all',
        'since': one_week_ago,
    }

    # Fetch pull requests from the GitHub API
    response = requests.get(base_url, headers=headers, params=params)

    # Check if the request was successful, then capture the data in json format
    if response.status_code == 200:
        pull_requests = response.json()
       
        # Sort pull requests by state (opened, in progress, closed)
        sorted_pull_requests = sorted(pull_requests, key=lambda pr: pr['state'])


        # Print detailed information for each pull request
        print(f'Detailed information for {owner} / {repo} pull requests in the last week:')
        
        #Start the counting for PR's state at zero
        open_pr = 0 
        closed_pr = 0
        merged_pr = 0 
        
        # Looping through the json object getting the desired fields
        for pr in sorted_pull_requests:
            print(f'\nPull Request #{pr["number"]}')
            print(f'Title: {pr["title"]}')
            print(f'Author: {pr["user"]["login"]}')
            print(f'Created At: {pr["created_at"]}')
            print(f'Updated At: {pr["updated_at"]}')
            print(f'Closed At: {pr["closed_at"]}')
            print(f'State: {pr["state"]}')  

            #Once this has been collected, it can be included on a dict for further usage      
            if pr["state"] == "open":
                open_pr = open_pr + 1 
            elif  pr["state"] == "closed":
                closed_pr = closed_pr + 1
            elif pr["state"] == "merged":
                merged_pr = merged_pr + 1
        
        print(f"\n\nTotal number of PR, Open, Merged, Closed PR for {owner} / {repo}:\n")
        print(f"Total number of PR: {len(sorted_pull_requests)}")
        print(f"Open PR = {open_pr}")
        print(f"Merged PR = {merged_pr}")
        print(f"Closed PR = {closed_pr}")
    else:
        print(f'Error: Unable to fetch data from GitHub API. Status code: {response.status_code}')

if __name__ == '__main__':
    # Replace these values with your GitHub repository information
    owner = 'nodejs'
    repo = 'node'
    # Replace 'your_token' with your GitHub personal access token
    token = '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'

    get_pull_requests_details(owner, repo, token)
