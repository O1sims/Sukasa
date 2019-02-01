FROM python:3.6

# Set up apt-get
RUN apt-get -qq update

# Download Python framework and dependencies
RUN apt-get install -qq -y build-essential libffi-dev python-dev

# Set up the Django framework
RUN mkdir /sukasa
WORKDIR /sukasa
ADD requirements.txt /sukasa/
RUN pip install -r requirements.txt

# Expose ports
EXPOSE 5000
