FROM python:3.9-alpine

RUN pip3 install zmq
RUN pip3 install flask

WORKDIR /app