# Satellite Simulation

This is a project created to simulate satellite updates and allow you to change the status in real time.

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

To run the application locally, once Docker is installed, run this command from the satellite-simulation folder to deploy with Docker compose.

```
$ docker compose up -d
[+] Building 5.0s (14/14) FINISHED
...
=> [web] resolving provenance for metadata file
[+] Running 3/3
...
Attaching to celery-container, redis-container, satellite-project-container
```

After the application starts, navigate to `http://localhost:8000` in your web browser to verify it is running.

If you want to create a superuser for django, you can run this command to create an admin user.

```
$ docker exec -it satellite-project-container python manage.py createsuperuser
```
You can also run this command in the django container exec to add an admin user instead.

```
python manage.py createsuperuser
```
This superuser will allow you to open the admin panel to add and manage spacecrafts: `http://localhost:8000/admin`

You can also directly access the API directly: `http://localhost:8000/api/docs`

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
- Every time a status changes, send an alert to the frontend (pub/sub, websocket, etc.), and update the status in the database.

#### Frontend

- The frontend can be very basic. Its only purpose is to show off the statuses for each spacecraft.
- List each spacecraft and its associated status. Add a button for each spacecraft that will update 'MALFUNCTIONING' statuses to 'NOMINAL'.

### Implementation

#### Initial Thoughts

For time constraints, I will need to keep this project scoped to MVP and then add lower and mid-priority tasks only if I have time.  
The main MVP concepts are:

- Allow CRUD operations for satellites, with an ENUM status NOMINAL, MALFUNCTIONING
- Create some sort of event driven architecture that alerts the client of a change.
- Containerize the application for easy testing 
- A Basic front end

For the backend, I decided to use Django because it has built-in security roles, it uses python similar to this position, and I want to dig deeper into Django's abilities to handle real time communication.

I was debating on using websockets but to decouple the connection and less complexity, I decided to use Server Side Events.  I also wanted to avoid using the cloud infrastructure at this time to keep it simple and SSE should be quick for a MVP that can be extended if needed. For the front-end I was thinking about adding a separate react front end. If I have time, I might either add it to the project or just build something quick using Django views.

#### Priority List

Normally I would use a Kanban project like in `https://kanbanflow.com/` to manage the priorities and backlog for personal projects but for ease of use and ease of following, I will just update this word document to help give a description of my approach:

##### High-Priority

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
        Allow CRUD operations for satellites, with a status NOMINAL or MALFUNCTIONING
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

#### Mid-Priority

<ul>
    <li>Split Localhost and Production Template</li>
    <li>Basic unit test example</li>
    <li>Mock results for testing</li>
    <li>Update the database to Postgres</li>
    <li>React front end</li>
</ul>

#### Low-Priority

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

#### Last minute changes in thought

When using SSE, the ideal route would be to allow triggers from the database.  At this point, the example I was using pushed updates from the endpoint but not from a trigger on the database.  This can work, but is not ideal as the trigger should come from the database.

Ideally, create a CRON to update the database, the database will trigger an event that SSE is watching on.  When that event happens then trigger the update…(Note CRON’s only run every minute, so went into creating tasks using Celery Beat’s and Redis. For now just going to add the update task into the simulation and maybe add beats later if time to decouple the simulation)

The current SSE structure is basically polling but from the server side at intervals similar to polling.  This is better than polling on the client side because it is close to the data, but still not ideal as it is based on a timer.

A better solution would be watching the database and having it ‘signal’ the trigger from the insert.  Not quite sure how to do this in Django at the moment, still looking for solutions.

<b>Internal thought:</b> for now run SSE based on a timer that looks up the database.  The ideal solution here would only push the changes needed.  I was thinking of storing the state on the backend then searching through it and only sending the updated items.  This could be from the lastUpdatedDate compared to when the SSE was started.  That would allow a lookup on the state to see what items changed. This doesn’t seem ideal, but could be developed quickly to meet the deadline and allow less network traffic from the front end.

<b>Last Push:</b> Goal is to get some data into the front end and refactor the event_stream after. There are many Websocket tutorials out there and it might have been an easier choice for a quicker delivery. That being said, I still like the one way connections with SSE opposed to bi-directional flow as I think it might be harder to load balance, use with firewalls and proxies.(It just takes more time than I thought to set up) 

<b>Last issue working on:</b> celery is not working anymore once containerized. It doesn’t seem to be loading the models from django.  I’m taking a deeper look into this.

### Results


##### Landing Page

![Landing Page](https://github.com/Justin-jay-Kirkman/satellite-simulation/blob/main/img/landing.jpg)

##### Admin Page

![Admin Page](https://github.com/Justin-jay-Kirkman/satellite-simulation/blob/main/img/Admin.jpg)

##### API

![API](https://github.com/Justin-jay-Kirkman/satellite-simulation/blob/main/img/API.jpg)

##### FrontEnd

![Vue FrontEnd](https://github.com/Justin-jay-Kirkman/satellite-simulation/blob/main/img/frontend.jpg)


#### Final Thoughts
This was a fun project that allowed me to dig deeper into researching, exploring different technologies and ramping up into some unfamiliar territories.
Setting up my docker containers was frustrating at times, but fun. Keeping this project as minimal as possible was a challenge as there were so many things I wanted to add to it. 
When I created the github check-ins I tried to keep them grouped by feature, so hopeful this can be a good training examples for others.

As far as meeting the requirements for the project, I trust I was fairly close. I created an CRUD API that can be accessed quite easily if other apps need to use it. Security can easily be added to it and CORS can be added per IP fairly easy. 
Celery is setup and allows Tasks to run and display in the Django Admin pages.  Django Admin also allows quick CRUD actions instead of using the API if desired.
The Celery Task when in a container currently is not able to access the models for some reason.  I could add celery beats, though the task is running just not reading correctly so having it scheduled add little.
The frontend is connecting to the SSE, I just need to add the update button, state and display at this point.
I trust the documentation of this project is good to give a flavor of my approach and thought process as well as my ability to show I can learn/implement new technologies in a short period of time. 

#### After deadline
##### CELERY!!!
I desired to get celery to work under containers but couldn’t get it to write to the correct database.  When using sqlite, I noticed that it was writing outside the containers to my localhost database so I figured it was a setting.  To get around this I tried to change where celery read from the django models, but couldn’t figure out how to change it.  I googled suggestions and people pointed me to adding `CELERY_RESULT_BACKEND_DB` to the database directly.  I tried this to no avail.  I even set up Postgres to run in a separate container but was having issues with it connecting.  This issue took longer than the whole rest of the project to debug and so I tabled it for the time being. (I even ran old containerized projects from github and they were having separate issues with missing celery library versions during compose up…) I decided to add the random updates from the front end instead.

##### vue.js
I added vue.js on the front end as a separate SPA and with login permissions for future updates. The front end is now functioning with SSE loading after bypassing Celery.

