# python-docker

A simple Python app for [Docker's Python Language Guide](https://docs.docker.com/language/python).

# DFF Copied Over

- I copied over some of the scripts from the website to make easier to cut and paste.

## Run a simple test.

```
# This is not necessary becaise I am in the directory
# cd /path/to/python-docker

# Create a virtual environment. https://docs.python.org/3/library/venv.html
python3 -m venv .venv

# Activate the virtual environment.
source .venv/bin/activate

# Install dependencies. This is an example of one of the 12 Factor Rules --> Declare dependencies.
(.venv) $ python3 -m pip install -r requirements.txt

# Run the application and access from a browser
(.venv) $ python3 -m flask run

# CNTL-C to end application

# Exit virtual environment.
deactivate
```

## Docker

- The command example is in beta and I am not using that version of Docker.


- So, I went old school and wrote the files following a different example.  https://medium.com/geekculture/how-to-dockerize-your-flask-application-2d0487ecefb8

- Commands:
  - ```docker build -t donff2j/e6156-flask .```
  - ```docker images``` (I have a lot of images)
  - ```docker run -p 5001:5001 donff2j/e6156-flask```
  - ```docker push donff2j/e6156-flask``` (This step pushed an image for your architecture)

- I committed and pushed the project. 

## EC2

- I used an Amazon Linux instance.


- I followed this example: https://medium.com/appgambit/part-1-running-docker-on-aws-ec2-cbcf0ec7c3f8
  - ```sudo yum update -y```
  - ```sudo service docker start```
  - ```sudo usermod -a -G docker ec2-user```
  - I also installed Git.


- I cloned the project instead of pulling the container because my Mac is ARM.
  - docker build  . -f cool


- There is a way to "build" on ARM for an Intel chipset. I am lazy.


- I built the Dockerfile and then used ```curl localhost:5001```


- I now need to modify the service group to get to port 5001. Go through the instance to security group and add a rule.


- Go into the console and get the EC2 instances public IP address. You can now access the app on 5001.


- Pull the Docker container ```docker pull donff2/e6156-flask```


- I used an Amazon Linux instance.
- 

## Some Helpful Commands

- Kill a proces# E6156 - Topic in SW Engineering: Cloud Computing docker-flask-sample

## Overview

This is a very, very simple example of how to
1. Build and run a simple Flask web application
2. Package with Docker
3. Push to Docker Hub
4. Pull onto an EC2 instance
5. Execute on EC2

## Foundation

I followed a simple [online tutorial.](https://docs.docker.com/language/python/build-images/)

Note: You must have installed Docker on your laptop and your EC2 instances.

There are some modifications and extensions, specifically:
1. I do not use "Flask run ... "
   1. I modified app.py so that you can run using python command.
   2. The CMD entry in the Dockerfile is different.
2. You must ensure that the Flask application sets host 0.0.0.0. The app.run() in app.py handles this requirement.
3. Please create a new environment for your project that includes the mimimum packages you require.
4. Make sure you update requirements.txt when you add packages (you can use pip freeze > requirements.txt)
5. I added a file scripts.sh that contains commands I ran. You will have to modify.
6. Make sure you have enabled access to port 5000 for your EC2 security group.
7. Make sure you try to connect to the public IP address/DNS for the EC2 instance.


