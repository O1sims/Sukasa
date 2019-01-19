FROM node:latest

RUN npm install -g typescript

# Install dependencies
RUN mkdir /gui
WORKDIR /gui
ADD gui /gui
RUN npm install

# Transpile Typescript
RUN tsc

# NPM start
CMD npm run lite
