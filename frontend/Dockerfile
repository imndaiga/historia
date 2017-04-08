FROM node:latest
MAINTAINER squarenomad

ADD . /app
WORKDIR /app
RUN npm install
EXPOSE 3000

CMD ["npm","run","deploy"]