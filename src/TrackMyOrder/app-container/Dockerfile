FROM python:3.11.0-alpine

EXPOSE 5000

RUN apk update && apk upgrade && \
    apk --no-cache add libaio libnsl libc6-compat curl unzip

RUN apk add build-base libressl libffi-dev libressl-dev libxslt-dev libxml2-dev xmlsec-dev xmlsec
RUN apk add --no-cache --upgrade build-base bash

COPY . /track-my-order/app-container
RUN pip3 install -r /track-my-order/app-container/config/requirements.txt

RUN bash /track-my-order/app-container/setup.sh

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

RUN adduser -D -u 5679 tmoappuser && chown -R tmoappuser /track-my-order
USER tmoappuser

RUN mkdir /track-my-order/log/
RUN mkdir /track-my-order/log/gunicornlogs/

RUN touch /track-my-order/log/gunicornlogs/access.log
RUN touch /track-my-order/log/gunicornlogs/error.log

WORKDIR /track-my-order/app-container/

CMD ["sh", "/track-my-order/app-container/service.sh"]