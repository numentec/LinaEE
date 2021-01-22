FROM node:lts
RUN mkdir linafe
WORKDIR /linafe
COPY package*.json ./
RUN npm install
COPY . .