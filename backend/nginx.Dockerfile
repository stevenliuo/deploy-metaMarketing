FROM node:20.14.0-alpine AS builder

RUN mkdir /front

WORKDIR /front

COPY /frontend/yarn.lock /front

COPY /frontend/package.json /front

RUN yarn install

COPY /frontend /front

RUN yarn build


FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY --from=builder front/dist /usr/share/nginx/html

COPY nginx/nginx.conf.template /etc/nginx/templates/