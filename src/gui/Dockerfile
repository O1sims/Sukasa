# base image
FROM node:latest

# set working directory
RUN mkdir -p /gui/app
WORKDIR gui/app
ADD app/package.json /gui/app
RUN npm install

# Start app
CMD npm run lite
