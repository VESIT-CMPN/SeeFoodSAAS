# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
WORKDIR /app

ADD ./requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

ADD . /app

RUN pip3 install darkflow/. --upgrade

# Make port 4000 available to the world outside this container
EXPOSE 4000

WORKDIR /app/seefoodSAAS

CMD ["python3", "manage.py", "runserver", "0.0.0.0:4000"]
