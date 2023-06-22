FROM node:14.4.0-alpine3.10 as build-stage
USER root

WORKDIR /frontend-deploy
COPY package.json /frontend-deploy
RUN npm install
COPY . /frontend-deploy
RUN npm run build

FROM nginx:1.15
COPY --from=build-stage /frontend-deploy/build/ /usr/share/nginx/html
COPY --from=build-stage /frontend-deploy/nginx-proxy.conf /etc/nginx/conf.d/default.conf
