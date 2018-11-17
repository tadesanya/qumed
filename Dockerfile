FROM python:3.6

ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /qumed

# Set the working directory to /qumed
WORKDIR /qumed

# Copy and install requirements
COPY requirements.txt /qumed/
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /qumed
COPY . /qumed/

# Make port 8000 available to the world outside this container
EXPOSE 8000
