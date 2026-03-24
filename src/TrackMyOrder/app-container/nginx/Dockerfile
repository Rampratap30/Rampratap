FROM nginx:1.24.0-alpine-slim

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/

RUN rm /etc/nginx/conf.d/default.conf
COPY project.conf /etc/nginx/conf.d/

#RUN mkdir /trackmyorder

COPY sites ./sites
#COPY sites /app/trackmyorder/sites
#COPY assets/images ./assets/images
#COPY assets/icons ./assets/icons