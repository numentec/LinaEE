FROM python:latest
LABEL maintainer="Numentec"
ENV PYTHONUNBUFFERED 1
RUN mkdir linabe
WORKDIR /linabe
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x dj.sh
RUN echo "America/Panama" > /etc/timezone