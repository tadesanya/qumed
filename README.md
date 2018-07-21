# Qumed

### Setup
Create a virtualenvwrapper with python3 as the default python exe:
`mkvirtualenv --python=/usr/bin/python3 qumed`

Clone the repo:
`git clone git@bitbucket.org:qumed/qumed.git`.
This uses SSH, read this to setup SSH on your system: https://confluence.atlassian.com/bitbucket/set-up-an-ssh-key-728138079.html

Alternatively you can use HTTPS:
`git clone https://tadesanya@bitbucket.org/qumed/qumed.git`

Setup a postgres database

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

While in your virtualenvwrapper, install all the packages needed
`pip install -r requirements.txt`

Run Migragrations `python qumed/manage.py migrate`

Start server `python qumed/manage.py runserver`

### Structure
The Repo has a main branch `master`. 
All other branches checkout from it.