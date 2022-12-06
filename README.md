# Backend controller

There are 3 types of components:
- Manipulator
- Controller
- Sensor

This package defines the comunication between them.


# Testing

To test all components run `docker compose up`

# Manipulator

This component is only listening to **Controller**'s messages on TCP connection.

You can specify port for accepting the TCP connection.

## Usage
```
$ python3 manipulator/manipulator.py -h
```
```
usage: manipulator.py [-h] [-p PORT]

Proccess messages got from the controller

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port to listen the tcp connection (default: 10000)
```

# Sensor

Connects to the **Controller** via TCP to help it discover the sensor's publisher address. Then posts randomly generated messages 300 times per second. 

Sensor acts as Publisher in PUB/SUB pattern in ZeroMQ.

## Usage
```
$ python3 sensor/sensor.py -h
```
```
usage: sensor.py [-h] [-p PORT] -d DESTINATION [-t TIMES_PER_SECOND]

Publish sensor messages

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port to publish messages on (default: 5000)
  -d DESTINATION, --destination DESTINATION
                        destination(controller) address (example: 0.0.0.0:30000)
  -t TIMES_PER_SECOND, --times-per-second TIMES_PER_SECOND
                        number of times per second the sensor sends a message(default: 300)
```

# Controller

Connects to **Manipulator** and listens on multiple **Sensors**. Then every 5 seconds decides on the control signal for **Manipulator** using messages got after last decision.

Controller has a Flask server, on which the last control signal is served.

## Usage

```
$ python3 controller/controller.py -h
```
```
usage: controller.py [-h] -d DESTINATION [-p PORT]

controller

optional arguments:
  -h, --help            show this help message and exit
  -d DESTINATION, --destination DESTINATION  manipulator(destination) address (example: 0.0.0.0:10000)
  -p PORT, --port PORT  port to listen for new sensors (default: 30000)
```