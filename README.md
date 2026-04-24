# ADA502Gruppe5

## Trello
https://trello.com/b/juFPn2S1/ada502gruppe5

## Landing page
http://158.37.66.185/

## How to update the documentation website (in the future)
Step 1: Make changes to index.md in the "docs" folder in the "web-docs" folder.


Step 2: Use cd to move from project root to web-docs -> "cd web-docs"


Step 3: Build the webpage -> "mkdocs build" (Command must be used in the web-docs folder)


### NOTE: You can also make direct changes to the index.html file obviously, in that case skip steps 1-3.


Step 4: Check that your changes have been added. Run the docker-compose file and test on localhost:8000 to see changes.


Step 5: Push changes to the repository, hopefully there will soon be an automatic CD pipeline up and running.


Step 6: Test the landing page using the above url.


https://www.mkdocs.org/getting-started/

## MQWorkerService
https://github.com/h572659/MQWorkerService

## To host locally
Because of troubles we have had with keycloak (kc) and https the kc logic is mostly commented out, but if it is run locally it should work.

To run this locally follow these steps:
1. Clone the project
2. Make sure sure you have docker installed
3. To have localhost change the following: In auth comment out line 9, 10 and 15 and remove comment from line 12, 13 and 17.
4. To enable kc remove comments in main from line 46, 54 and 71.
5. Then run "docker compose up --build -d"

Head to http://localhost:8000/docs and our endpoints should appear.
To acess these click authorize and you can create your own user which will be given the user role or log into username: "User1" Password: "User1" for admin and username: "User2" Password: "User2" for user role. Only these to users are saved so newly created users wont be remembered when you throw away the container.
