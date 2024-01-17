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
from sendComms import emailCompose
from setUpVariables import owner, repo, token, time, fileNamePath, sender_email, receiver_email

# Function which queries github for pull requests 

def getPullRequests_details(owner, repo, token, time):
    base_url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    headers = {'Authorization': f'token {token}'}
    
    # Calculate the date time weeks ago
    number_of_week_ago = (datetime.now() - timedelta(weeks=time)).isoformat()

    # Define parameters for the GitHub API request
    params = {
        'state': 'all',
        'since': number_of_week_ago
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
        #Start the counting for PR's state at zero
        open_pr = 0 
        closed_pr = 0
        merged_pr = 0 
        
        # File being created new, then info attached on it
        attachMail = open(fileNamePath,"w")

        # Looping through the json object getting the desired fields, and adding format to this file
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

        # Changing information display order, first the counting, then details, and formatting it as HTML
        with open(fileNamePath,"r") as appndFile:
            save = appndFile.read()
        with open(fileNamePath,"w") as appndFile:
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
        
        emailCompose(f"Total number of PR, Open, Merged, Closed PR for {owner} / {repo}:",fileNamePath)

def printMessageConsole():
    # Print detailed information for each pull request
    print(f'Subject: Detailed information for {owner} / {repo} pull requests in the last week:\n')
    print(f"From:{sender_email}\n")
    print(f"To:{receiver_email}\n")
    print(f"Subject: Total number of PR, Open, Merged, Closed PR for {owner} / {repo}:\n")
    print("email sent using MIME/UTF-8 and HTML file type")
    print("Message: \n")

    with open(fileNamePath,"r") as showContent:
            messageBody = showContent.read()
            print(messageBody)
    showContent.close()
    print("EOM \n")



if __name__ == '__main__':
    # All variables have been set on a configuration file. 
    # Gathering the information from githup APIm once done internally calls for a function to format the output and calls for email send
    getPullRequests_details(owner, repo, token, time)

    # Print email into the console
    printMessageConsole()
