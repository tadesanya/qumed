# Qumed

### Setup
Create a virtual environment with python3 as the default python exe:
`mkvirtualenv --python=/usr/bin/python3 qumed`

Clone the repo:
`git clone https://tadesanya@bitbucket.org/qumed/qumed.git`

Setup a postgres database

Create an `.env` file in the base directory of the project (usually the directory that has the manage.py file in it).
Here you set environment variables:
```python
SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEBUG=True
DATABASE_URL=postgres://user:password@host:5432/mydb
```
