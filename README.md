# E6156 - Topic in SW Engineering: Cloud Computing docker-flask-sample

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


