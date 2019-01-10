# Qumed

### Setup on development environment
Create a virtual environment `qumed` with virtualenvwrapper, using python3 as the default python exe:
`mkvirtualenv --python=/usr/bin/python3 qumed`

Clone the repo:
`git clone git@bitbucket.org:qumed/qumed.git`.
This uses SSH, read this to setup SSH on your system: https://confluence.atlassian.com/bitbucket/set-up-an-ssh-key-728138079.html

Alternatively you can use HTTPS:
`git clone https://tadesanya@bitbucket.org/qumed/qumed.git`

Install Docker (https://www.docker.com/get-started)

Create an `.env` file in the base directory of the project (usually the directory that has the manage.py file in it).
Here you set environment variables:
```python
SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEBUG=True
DATABASE_URL=postgres://<database_user>:<database_password>@<database_host>:<database_port>/<database_name>
HOSTS=127.0.0.1,localhost,localhost:8000,127.0.0.1:8000
EMAIL_wdHOST=XXXXXXXXXXXXXXXXXXX
EMAIL_PORT=XXX
EMAIL_HOST_USER=XXXXXXXXXXXX
EMAIL_HOST_PASSWORD=XXXXXXXXXXXXXXXXXXX
EMAIL_USE_TLS=True
```

To start the server, in the root directory (the folder named 'qumed' that has the files Dockerfile, docker-compose.yml and README.md in it), run the command `docker-compose up`. Go to `localhost:8000` or `0.0.0.0:8000` in your browser to view the app.

To shut down the server, in the root directory either run the command `docker-compose down` or use the keyboard shortcut `CTRL+C`

### Structure
The Repo has a main branch `master`. 
All other branches checkout from it.