FROM node:latest
MAINTAINER squarenomad

ADD ./package.json /app/package.json
WORKDIR /app
RUN npm install
ADD . /app
RUN npm run build
EXPOSE 3000

CMD ["npm","run","start"]