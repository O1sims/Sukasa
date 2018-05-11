FROM ubuntu:16.04

# Set up apt-get
RUN apt-get -qq update
RUN apt-get -qq -y install curl

# Download Python framework and dependencies
RUN apt-get update
RUN apt-get -y install python-pip python-dev build-essential python-software-properties
RUN apt-get -y install python-tk
RUN apt-get -y install python-bs4

# Download Node and NPM
RUN curl -sL https://deb.nodesource.com/setup_7.x | bash -
RUN apt-get -y install nodejs
RUN apt-get -y install g++

# Set up Django framework
RUN mkdir /Kasa
WORKDIR /Kasa
ADD requirements.txt /Kasa/
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

# Add the Kasa directory
ADD . /Kasa/

# Install Angular packages
# WORKDIR /Kasa/gui/app
# RUN npm install

# Expose ports
EXPOSE 8000