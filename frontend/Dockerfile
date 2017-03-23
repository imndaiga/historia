FROM node:latest
MAINTAINER squarenomad

ADD . /app
WORKDIR /app
RUN npm install
EXPOSE 8080

ENTRYPOINT ["npm"]
CMD ["run","dev"]