FROM node:latest

# Install dependencies
RUN mkdir /gui
WORKDIR gui
ADD gui/package.json /gui
RUN npm install

# NPM start
CMD npm run lite
