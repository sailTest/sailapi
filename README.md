
The following python application gather information about pull requests from one week agon, from any GitHub repository and send an email with the information of the total number of open, closed and merged pull requests during that period of time.


This solution can be run by cloning the repository and then, configuring the required parameters into the setUpVariables.py file, where all the needed information must be provided. Also, from that file, the name of the repository and its owner must be provided.

Once the information has been correctly populated, the docker image can be created and executed once is completed. 

The description of the files is as follow



For Dockerfile creation:


dependencies.txt - Has the additional python modules this application needs
Dockerfile - The actual dockerfile which helps to contenarize this application 

For handling the API request  and sending the email:


githubQuery - python script which does the actual query, additional functions where set up inside to help format the file and printing in console


sendComms.py - python script which is in charge of sending emails 


setUpVariable.py - a file where all variables must be declared, as best practive to minimize hardcoding


Software requirements
Requirements: python 3.11 or above and docker (podman could be used too)
