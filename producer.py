#!/usr/bin/env python

from random import choice
from confluent_kafka import Producer

if __name__ == '__main__':

    config = {
        # User-specific properties that you must set
        'bootstrap.servers': 'localhost:57891',

        # Fixed properties
        'acks': 'all'
    }
    topic = "purchases"
    # Create Producer instance
    producer = Producer(config)

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    
    # Produce data by selecting random values from these lists.
    
    user_ids = "sujal sinha "
    products = "Sujal this side "

    
    producer.produce(topic, products, user_ids)
        

    # Block until the messages are sent.
    producer.poll(100)
    producer.flush()