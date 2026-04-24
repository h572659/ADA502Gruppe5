# ADA502Gruppe5

## Introduction


This repository contains one of the two components of our prototype fire risk application, developed for the ADA502 - Cloud Computing course at HVL. The project uses data collected by the [meterologisk Institutt](https://www.met.no/)
 to assess fire risks in specific geographic locations. To perform these calculations, we utilize the [dynamic FRCM](https://pypi.org/project/dynamic-frcm/), which is based on a research paper.


## Vision

The project aims to support firefighters in making informed decisions about resource allocation. By redirecting personnel from areas with low fire risk to areas with high fire risk, the application seeks to improve efficiency and reduce fire-related losses.

## Structure

![Visual explanation](/images/project.png)


The application is designed as follows:

1. Data Collection: One component gathers data from the Meteorologisk Institutt (MET)

2. Calculation & Storage: This component performs fire risk calculations and stores the results in a relational database.
3. Publishing Updates: Calculated fire risk data is also sent to a broker, which provides hourly updates to subscribers.
4. Front-End Behavior: To accommodate users who may not want the application running continuously, the front-end reads the most recent fire risk data from the database on startup before connecting to the broker for live updates.

This forms the minimum viable concept of the application. Future development could allow users to view predictions for upcoming periods and review historical trends

## Some Comments on Our Database

Our current relational database contains three tables: users, city, and fire_risk.

1. city

- id: Primary key
- name: Name of the city
- latitude, 
- longitude: Spatial coordinates

The application can be easily extended by adding more cities or locations to this table.

2. fire_risk

- id: Primary key
- city_id: Foreign key linking to the city table
- timestamp: Timestamp provided by MET (in UTC)
- ttf: Fire risk value
- wind_speed: Wind speed value provided by MET
- is_forecast: Boolean indicating whether this is a prediction (true) or historical data (false)
- created_at: Timestamp when the calculation was added to the database

3. users

This final table is not currently in use but is intended to store login information in the future.

## Problems and missing parts

### Keycloak
Keycloak is currently not working on our landing page. You get contact to it when using the school network but then you get a missing https error, so we have chosen to remove it for now. They keycloak service doesnt have persistence yet so any new users and changes in the realm has to be exported manually. The keycloak part does work when locally hosting.

### The front page
A dedicated frontend has not yet been implemented. As a result, the application currently relies on basic endpoints (Swagger UI), making it less user-friendly and not visually appealing. 

### The FRCM part
In the API the FRCM part only collects the data from our database where we have only calculated for three locations. Its also unclear what locations you are requesting from because we use numbers 1-3. Where 1 is Oslo, 2 is Bergen and 3 is Trondheim. Its not userfriendly at its current stage.

### CI/CD
The CI/CD part works well but the tests in the CI part is barely existing.

## Landing page
http://158.37.66.185:8000/

This is the landing page for the current project where you should be able to check out the current state of the project. 


## MQWorkerService
https://github.com/h572659/MQWorkerService


This component is responsible for fetching data from the Meteorologisk Institutt (MET)
 once an hour. The data is processed using the dynamic FRCM library to calculate fire risk.

The results are:

Stored in the relational database for retrieval through the API component.
Sent to RabbitMQ, which provides updates to subscribers (e.g., the front-end application).

This service forms the automated backend of the system, ensuring that fire risk data is regularly updated and distributed.

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
