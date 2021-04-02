FROM python:latest
LABEL maintainer="Numentec"

RUN mkdir linabe
WORKDIR /linabe
COPY . .

# Installing Oracle instant client
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y libaio1
RUN echo /linabe/instantclient_12_1 > /etc/ld.so.conf.d/oic.conf \
    && ldconfig
ENV PATH=$PATH:/linabe/instantclient_12_1

# Installing Django and requirements
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
