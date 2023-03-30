FROM python:3.9.16-slim AS builder

# Update all the things
RUN apt-get update && apt-get -y upgrade

RUN apt-get -y install gcc libglib2.0-0


#copy in the app
COPY ./skybrush-server /skybrush-server
COPY ./skybrush-ext-controller-poc /skybrush-ext-controller-poc
COPY ./skybridge-ext-rl-gaming /skybridge-ext-rl-gaming
COPY ./flockwave-spec /flockwave-spec
WORKDIR /skybrush-server

#install poetry
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry lock 
RUN poetry install --no-dev