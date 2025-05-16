FROM node:lts-alpine3.19 as build-stage

WORKDIR /fe

COPY ./package*.json /fe
RUN npm install

COPY ./ /fe
RUN npm run build || true # gross hack

FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /fe/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]