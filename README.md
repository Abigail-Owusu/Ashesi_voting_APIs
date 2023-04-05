# Ashesi_voting_APIs
Design a REST API for Ashesi's electronic voting system to register and de-register students, update their information, create and delete elections, and allow voting. Retrieve information on registered voters and elections, including details on the latter and deploy it on google cloud

In the previous repository, the APIs for the voting system was not deployed globally. this project deploys the various APIs globally using google cloud functions.


#Stack

Backend: Python Framework: Flask Database: Firestore Deployment: google cloud

Instructions on how to set up

Make sure you have installed the modules in the requirements.txt(pip install -r requirements.txt)

This API has been deployed on google cloud. Below are the links to to test these APIs in Postman as per the instructions and attach set the HTTP methods as specified.

Check screenshots_deployment.pdf for information to go in the request body for some POST requests.

# Prompt 1 – Register a voter

Link : https://us-central1-voting-database-d7727.cloudfunctions.net/register_voter HTTP METHOD: POST

# Prompt 2 – Deregister a voter.

Link: https://us-central1-voting-database-d7727.cloudfunctions.net/deregister_voter?user_id=<voter_id> HTTP METHOD: DELETE

# Prompt 3 - Updating the register's voter.

Link: https://us-central1-voting-database-d7727.cloudfunctions.net/update_voter?user_id=<voter_id> HTTP METHOD: PUT

# Prompt 4 – Retrieving a registered voter

Link: https://us-central1-voting-database-d7727.cloudfunctions.net/get_voter?user_id=<voter_id> HTTP METHOD: GET

# Prompt 5: Register an Election in the database.

Link: https://us-central1-voting-database-d7727.cloudfunctions.net/register_election HTTP METHOD: POST

Prompt 6: Retrieving an Election with its details

Link: https://us-central1-voting-database-d7727.cloudfunctions.net/get_election?election_id=<election_id> HTTP METHOD: GET

# Prompt 7: Deleting an election

Link: https://us-central1-voting-database-d7727.cloudfunctions.net/delete_election?election_id=<election_id> HTTP METHOD: DELETE

# Prompt 8 – Voting in an election.

Link : https://us-central1-voting-database-d7727.cloudfunctions.net/vote_in_election?voter_id=<voter_id>&candidate_id=<candidate_id>&election_id=<election_id> HTTP METHOD: POST

Note that <voter_id>, <candidate_id> and <election_id> are variables and must me replaced with actual values instead when testing.
