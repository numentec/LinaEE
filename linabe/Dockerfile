FROM python:latest
LABEL maintainer="Numentec"

# Installing Oracle instant client
ARG DEBIAN_FRONTEND=noninteractive

RUN mkdir /opt/oracle

ADD instantclient_12_1/* /opt/oracle/instantclient_12_1/

RUN apt-get update && apt-get install -y libaio1

RUN echo /opt/oracle/instantclient_12_1 > /etc/ld.so.conf.d/oic.conf \
    && ldconfig

ENV PATH=$PATH:/opt/oracle/instantclient_12_1

# Installing Django and requirements
ENV PYTHONUNBUFFERED 1
RUN mkdir linabe

WORKDIR /linabe
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt