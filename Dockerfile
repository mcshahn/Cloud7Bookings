# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ENV GOOGLE_CLIENT_ID=318056048243-6adot3h6126usbta6r202puo7meibsng.apps.googleusercontent.com
ENV GOOGLE_CLIENT_SECRET=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
ENV SECRET_KEY=x1cuDp1tML0QEuLHbBbfatpVyYqDfjLuTrzqXe7Z
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

CMD [ "python", "app.py", "--host=0.0.0.0"]
