FROM node:latest
MAINTAINER squarenomad

ADD . /app
WORKDIR /app
RUN npm install
EXPOSE 3000

ENTRYPOINT ["npm"]
CMD ["run","dev"]