FROM node:latest

# Create directory for GUI
RUN mkdir /gui
WORKDIR /gui

# Install dependencies
RUN npm install -g typescript
ADD gui/package.json /gui
RUN npm install

# Install dependencies
ADD gui /gui

# Transpile Typescript
RUN tsc

# NPM start
CMD npm run lite
