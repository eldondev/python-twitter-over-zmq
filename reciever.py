import sys
import time
import zmq
import json

context = zmq.Context()

controller = context.socket(zmq.SUB)
controller.connect("tcp://localhost:5559")
controller.setsockopt(zmq.SUBSCRIBE, "")
poller = zmq.Poller()

poller.register(controller, zmq.POLLIN)

a = set()

while True:
    socks = dict(poller.poll())
    if socks.get(controller) == zmq.POLLIN:
        message = json.loads(controller.recv())
        a.update(message.keys())
        print message
