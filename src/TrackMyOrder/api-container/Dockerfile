FROM python:3.11.0-alpine

EXPOSE 5000

RUN apk update && apk upgrade && \
    apk --no-cache add libaio libnsl libc6-compat curl unzip 

RUN apk add build-base libressl libffi-dev libressl-dev libxslt-dev libxml2-dev xmlsec-dev xmlsec
RUN apk add --no-cache --upgrade build-base bash

# Install Oracle Client
RUN cd /opt && \
    mkdir oracle

RUN cd /opt/oracle && \
    mkdir lib

RUN cd /tmp && \
    curl -o instantclient-basiclite.zip https://download.oracle.com/otn_software/linux/instantclient/213000/instantclient-basiclite-linux.x64-21.3.0.0.0.zip && \
    unzip instantclient-basiclite.zip && \
    cp -r instantclient_21_3/* /opt/oracle/lib && \
    rm -rf instantclient-basiclite.zip && \
    rm -rf instantclient_21_3 && \
    cd /lib && \
    ln -s /lib64/* /lib && \
    ln -s libnsl.so.2 /usr/lib/libnsl.so.1 && \
    ln -s libc.so /usr/lib/libresolv.so.2

COPY . /track-my-order/api-container
RUN pip3 install -r /track-my-order/api-container/config/requirements.txt

RUN bash /track-my-order/api-container/setup.sh

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
ENV ORACLE_HOME=/opt/oracle
ENV LD_LIBRARY_PATH=/opt/oracle/lib

RUN adduser -D -u 5679 tmoapiuser && chown -R tmoapiuser /track-my-order
USER tmoapiuser

RUN mkdir /track-my-order/log/
RUN mkdir /track-my-order/log/gunicornlogs/

RUN touch /track-my-order/log/gunicornlogs/access.log
RUN touch /track-my-order/log/gunicornlogs/error.log

WORKDIR /track-my-order/api-container/

CMD ["sh", "/track-my-order/api-container/service.sh"]