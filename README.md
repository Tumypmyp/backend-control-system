# Backend control system

In a control system exists 3 types of components:
- *Manipulator*
- *Controller*
- *Sensor*

This package defines the network comunication between them.

# Installation

```
git clone https://github.com/Tumypmyp/backend-control-system
cd backend-control-system/
```
# Run

To run all components:
```
docker compose up
```

# Components

All components use `python` scripts to communicate.

## Manipulator

This component is listening to *Controller*'s messages on TCP connection and prints them to logs.

### Usage
```
python3 manipulator/manipulator.py -h
```
```
usage: manipulator.py [-h] [-p PORT]

Proccess messages got from the controller

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port to listen the tcp connection (default: 10000)
```

## Sensor

Connects to the *Controller* via TCP to send his Publisher address. Then post randomly generated messages 300 times per second using this address.

*Sensor* acts as a Publisher in PUB/SUB pattern in ZeroMQ.

Signal messages published in `json` format:

```
{
 "datetime": "%Y%m%dT%H%M%S",
 "payload": "int"
}
```

### Usage
```
python3 sensor/sensor.py -h
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

## Controller

Connects to *Manipulator* and listens on multiple *Sensors*. Then every 5 seconds decides on the control signal for *Manipulator* using signals got after previous decision.

*Controller* has a Flask server. The last control signal is served on `http://127.0.0.1:20000/status`

Control messages published in `json` format: 
```
{
 "datetime": "%Y%m%dT%H%M%S",
 "status": "up" | "down"
}

```

### Usage

```
python3 controller/controller.py -h
```
```
usage: controller.py [-h] -d DESTINATION [-p PORT]

controller

optional arguments:
  -h, --help            show this help message and exit
  -d DESTINATION, --destination DESTINATION  manipulator(destination) address (example: 0.0.0.0:10000)
  -p PORT, --port PORT  port to listen for new sensors (default: 30000)
```