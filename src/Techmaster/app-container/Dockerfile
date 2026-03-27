#FROM python:3.7.12-alpine
FROM python:3.11.0-alpine

RUN apk update && apk upgrade && \
    apk --no-cache add libaio libnsl libc6-compat curl unzip

# xmlsec dependencies
RUN apk add build-base libressl libffi-dev libressl-dev libxslt-dev libxml2-dev xmlsec-dev xmlsec
RUN apk add --no-cache --upgrade build-base bash

EXPOSE 5000
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

COPY . /tech-master/app-container
RUN pip3 install -r /tech-master/app-container/config/requirements.txt

RUN bash /tech-master/app-container/setup.sh

RUN adduser -D -u 5679 appuser && chown -R appuser /tech-master
USER appuser

RUN mkdir /tech-master/log/
RUN mkdir /tech-master/log/gunicornlogs/

RUN touch /tech-master/log/gunicornlogs/access.log
RUN touch /tech-master/log/gunicornlogs/error.log

WORKDIR /tech-master/app-container/

CMD ["sh", "/tech-master/app-container/service.sh"]