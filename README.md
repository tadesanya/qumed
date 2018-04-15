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
DATABASE_URL=postgres://user:password@host:5432/mydb
```

While in your virtualenvwrapper, install all the packages needed
`pip install -r requirements.txt`

Run Migragrations `python qumed/manage.py migrate`

Start server `python qumed/manage.py runserver`

### Structure
The Repo has two main branches `master` and `dev`. 
`dev` is where all branches checkout of and where all PR's are merged to. `dev` is the branch that is used on staging/test servers, while `master` is the branch used on production. 