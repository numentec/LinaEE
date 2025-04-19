FROM python:latest
LABEL maintainer="Numentec"

# Installing Oracle instant client
ARG DEBIAN_FRONTEND=noninteractive

RUN mkdir /opt/oracle

ADD instantclient_12_1/* /opt/oracle/instantclient_12_1/

RUN apt-get update && apt-get install -y libaio1 \
    && apt-get install -y git procps telnet \
    && apt-get install -y gettext \
    && apt-get install -y build-essential \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Setting up Oracle instant client
RUN echo /opt/oracle/instantclient_12_1 > /etc/ld.so.conf.d/oic.conf \
    && ldconfig

ENV PATH=$PATH:/opt/oracle/instantclient_12_1

# Installing Django and requirements
ENV PYTHONUNBUFFERED 1
RUN mkdir linabe

COPY ./celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

WORKDIR /linabe
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
