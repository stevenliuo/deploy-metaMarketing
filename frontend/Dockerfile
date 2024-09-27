FROM node:20.14.0-alpine

WORKDIR /front_app/

COPY yarn.lock package.json /front

RUN yarn install

COPY . /front_app

RUN chmod +x entrypoint.sh

ENTRYPOINT ["bash","/front-app/entrypoint.sh"]



