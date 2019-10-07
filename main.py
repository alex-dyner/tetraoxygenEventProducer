#!/usr/bin/env python

import json
import time

from eventproducer import EventProducer
from eventpublisher import EventPublisher

with open('config.json') as config_file:
    config = json.load(config_file)

event_producer = EventProducer(config["producer"])
event_publisher = EventPublisher(config["publisher"])
event_publisher.init()

while True:
    event = event_producer.produce()
    try:
        event_publisher.publish(event)
    except:
        time.sleep(1)
        event_publisher.init()

    delay_time = 0.004
    time.sleep(delay_time)

