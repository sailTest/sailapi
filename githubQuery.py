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
from sendinfo import emailCompose

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
        pullRequests = response.json()
       
        # Sort pull requests by state (opened, in progress, closed)
        sortedPullRequests = sorted(pullRequests, key=lambda pr: pr['state'])
        
        # Function to format the file to be sent through email
        messageFormater(sortedPullRequests,owner,repo)
                       
    else:
        print(f'Error: Unable to fetch data from GitHub API. Status code: {response.status_code}')

def messageFormater(sorted_pull_requests,owner,repo):
    # Print detailed information for each pull request
        print(f'Detailed information for {owner} / {repo} pull requests in the last week:')
        
        #Start the counting for PR's state at zero
        open_pr = 0 
        closed_pr = 0
        merged_pr = 0 
        
        # File being created new, then info attached on it
        attachMail = open("emailattachment.html","w")

        # Looping through the json dict getting the desired fields, and adding format to this file
        for i in range(len(sorted_pull_requests)):
            attachMail.write("<tr> \n")
            attachMail.write("<td>" + str(sorted_pull_requests[i]["number"]) + "  "  + sorted_pull_requests[i]["title"] + "  " + sorted_pull_requests[i]["user"]["login"] + "  " +sorted_pull_requests[i]["state"] + "</td>" +"\n")
            attachMail.write("</tr> \n")
            if sorted_pull_requests[i]["state"] == "open":
                open_pr = open_pr + 1 
            elif  sorted_pull_requests[i]["state"] == "closed":
                closed_pr = closed_pr + 1
            elif sorted_pull_requests[i]["state"] == "merged":
                merged_pr = merged_pr + 1
        
        attachMail.write("</table> \n")
        attachMail.write("</body> \n")
        attachMail.write("</html>")

        attachMail.close()

        with open("emailattachment.html","r") as appndFile:
            save = appndFile.read()
        with open("emailattachment.html","w") as appndFile:
            appndFile.write("\n")
            appndFile.write("<!DOCTYPE html> \n")
            appndFile.write("<html> \n")
            appndFile.write(f"<h1>Total number of PR, Open, Merged, Closed PR for {owner} / {repo}</h1> \n")
            appndFile.write("<body> \n")
            appndFile.write("<table> \n")
            appndFile.write("<tr> \n")
            appndFile.write(f"<td> Total number of PR: {len(sorted_pull_requests)} </td>\n")
            appndFile.write("</tr> \n")
            appndFile.write("<tr> \n")
            appndFile.write(f"<td> Open PR = {open_pr} </td>\n")
            appndFile.write("</tr> \n")
            appndFile.write("<tr> \n")
            appndFile.write(f"<td>Merged PR = {merged_pr} </td>\n")
            appndFile.write("</tr> \n")
            appndFile.write("<tr> \n")
            appndFile.write(f"<td>Closed PR = {closed_pr} </td>\n")
            appndFile.write("</tr> \n")
            appndFile.write("</table> \n")
            appndFile.write("\n\n")
            appndFile.write("<h1>Detailed information about PRs is as follow: </h1>\n\n")
            appndFile.write("<table> \n")
            appndFile.write("<tr> \n")
            appndFile.write("<th> PR Number </th>\n")
            appndFile.write("<th> Title </th>\n")
            appndFile.write("<th> Author </th>\n")
            appndFile.write("<th> Status </th>\n")
            appndFile.write("</tr> \n")
            appndFile.write("</table> \n")
            appndFile.write("<table> \n")
            appndFile.write(save)
        appndFile.close()
        
        emailCompose(f"Total number of PR, Open, Merged, Closed PR for {owner} / {repo}:","emailattachment.html")


if __name__ == '__main__':
    # Replace these values with your GitHub repository information
    owner = 'grafana'
    repo = 'grafana'
    # Replace 'your_token' with your GitHub personal access token
    token = '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'

    get_pull_requests_details(owner, repo, token)
