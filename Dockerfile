FROM python:3.9-alpine

RUN pip install zmq

WORKDIR /app