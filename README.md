# Backend controller

There are 3 types of components:
- Manipulator
- Controller
- Sensor


# Testing

To test all components run `docker compose up`

# Manipulator

This component is only listening to **Controller**'s messages on TCP connection.

You can specify the port for the TCP connection.

## Example
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

Connects to the **Controller** via TCP to help it discover the sensor. Then posts generated messages as Publisher with ZeroMQ.

## Example
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

Connects to **Sensors** and **Manipulator**. Then every 5 seconds decides on the control signal for **Manipulator** using messages got after last decision.

## Usage

```
$ python3 controller/controller.py -h
```
```
usage: controller.py [-h] -d DEST [-p PORT]

controller

optional arguments:
  -h, --help            show this help message and exit
  -d DEST, --dest DEST  manipulator(destination) address (example: 0.0.0.0:10000)
  -p PORT, --port PORT  port to listen for new sensors (default: 30000)
```