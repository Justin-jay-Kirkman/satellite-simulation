# Satellite Simulation

This is a project created to simulate satellite updates and allow you to change the status.

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#run-the-application">How To Run Locally</a></li>
      </ul>
    </li>
    <li>
      <a href="#project-details">Project Details</a>
      <ul>
        <li><a href="#Description">Description</a></li>
        <li><a href="#Requirements">Requirements</a></li>
        <li><a href="#Implementation">Implementation</a></li>
        <li><a href="#Results">Results</a></li>
      </ul>
    </li>
  </ol>
</details>

## Getting Started

### Prerequisites
You will need to have <a href="https://www.docker.com/products/docker-desktop/">docker installed</a> and some knowledge of <a href="https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository">how to clone from github</a>.

### Run the Application

To run the application locally, once Docker is installed, run this command from the satellite_project folder to deploy with Docker compose.

```
$ docker compose up -d
Container satellite-simulation-web-1 Running
[+] Building 0.6s (11/11) Finished
...
=> [web] resolving provenance for metadata file 
```

After the application starts, navigate to `http://localhost:8000` in your web browser to verify it is running.

If you want to create a superuser to for django, you can run this command to create an admin user.

```
$ docker exec -it satellite-simulation-web-1 python manage.py createsuperuser
```
This suporuser will allow you to open the admin panel: `http://localhost:8000/admin`

Once you are done, you can stop and remove the containers using this command.
```
$ docker compose down
```

## Project Details

### Description

You are a spacecraft software engineer and your job is to create a simple satellite simulation.

### Requirements

Your task is to design a full-stack application that creates satellites, updates their status, and updates a database. CRUD

Please dockerize this application to make it easier to test. Language choice is up to you. If there are any questions, use your best judgment and explain why you chose to go that route. There are no wrong choices as long as the basic requirements are met.

Please give a description of your approach for this assignment.

#### Backend

- Add an endpoint that creates a spacecraft with an ID and a status (NOMINAL, MALFUNCTIONING). Add this spacecraft to a database (including status).
- Add endpoints that allow users to update the spacecraft status. (Other instances will see status updates through pub/sub, websocket, etc.)
- The statuses should also randomly change over time.
- Every time a status changes, send an alert to the frontend (pub/sub, websocket, etc), and update the status in the database.

#### Frontend

- The frontend can be very basic. Its only purpose is to show off the statuses for each spacecraft.
- List each spacecraft and its associated status. Add a button for each spacecraft that will update 'MALFUNCTIONING' statuses to 'NOMINAL'.

### Implementation

#### Initial Thoughts

For time constraints, I will need to keep this project scoped to MVP and then add lower and mid priority tasks only if I have time.  
The main MVP concepts are:

- Allow CRUD operations for satellites, with an ENUM status NOMINAL, MALFUNCTIONING
- Create some sort of event driven architecture that alerts the client of a change.
- Containerize the application for easy testing 
- A Basic front end

For the backend CRUD operations, I decided to use Django because it has built in security roles, it uses python similar to this position, I’ve been using it recently and want to dig deeper into ways to extend it for various other areas (maybe learn and take advantage of channels in Django) 

I was debating on using websockets but to decouple the connection and less complexity decided to use Server Side Events.  I also wanted to avoid using the cloud infrastructure at this time to keep it simple and SSE should be quick for a MVP that can be extended if needed. For the front-end I was thinking about adding a separate react front end. If I have time, I might either add it to the project or just build something quick using Django views.

#### Priority List

Normally I would use a Kanban project like in `https://kanbanflow.com/` to manage the priorities and backlog for personal projects but for ease of use and ease of following, I will just update this word document to help give a description of my approach:

##### High Priority

<ul>
    <li>
        Research Current trends on real time communication.
      <ul>
        <li>
            WebTransport - <span style="color:#4a84e0;">pass for now</span>
            <ul>
                <li>Newest, but less support at this time. Would be a fun side project</li>
            </ul>
        </li>
        <li>
            HTTP polling - <span style="color:#e0894a;">not efficient</span>
            <ul>
                <li>Maybe if we know there will always be an update at a certain time, but generally this is not recommended</li>
            </ul>
        </li>
        <li>
            AWS pub/sub - <span style="color:#e0704a;">too much setup</span>
            <ul>
                <li>Eventbridge could work as well or other cloud options, but it’s too much setup for this simple project.</li>
            </ul>
        </li>
        <li>
            WebSockets - <span style="color:#b8b500">considered</span>
            <ul>
                <li>
                    More setup than other solutions
                </li>
                <li>
                    Harder to scale than SSE
                </li>
            </ul>
        </li>
        <li>
            Server Side Events (SSE) - <span style="color:#6eb800;">chose this solution</span>
            <ul>
                <li>
                    One directional reads from the server
                </li>
                <li>
                    Updates can be done through HTTP calls
                </li>
            </ul>
        </li>
      </ul>
    </li>
    <li>
        Research Django SSE
    </li>
    <li>
        Allow CRUD operations for satellites, with an status NOMINAL or MALFUNCTIONING
        <ul>
            <li>Setup CRUD’s using Ninja</li>
        </ul>
    </li>
    <li>
        Containerize the application for easy testing 
    </li>
    <li>
        A Basic front end        
    </li>
  </ul>

#### Mid Priority

<ul>
    <li>Split Localhost and Production Template</li>
    <li>Basic unit test example</li>
    <li>Mock results for testing</li>
    <li>Update the database to Postgres</li>
    <li>React front end</li>
</ul>

#### Low Priority

<ul>
    <li>Create a Postman library to add regression tests</li>
    <li>Add Next.js</li>
    <li>Front end unit testing</li>
</ul>

#### Out of Scope

<ul>
    <li>
        AWS server setup and deployment
        <ul>
            <li>
                IoC w/ terraform
            </li>
        </ul>
    </li>
    <li>Create a websocket version or webTransport version for fun</li>
    <li>CI/CD Pipelines</li>
    <li>Linters and other development tools</li>
    <li>K8 Scaling</li>
</ul>