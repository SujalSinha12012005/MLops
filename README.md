# Kafka Python Demo

This repository contains two simple Python scripts demonstrating how to use Apache Kafka with the `confluent_kafka` Python client.

## Contents

- `consumer.py` – A Kafka consumer that reads messages from the `area` topic.
- `producer.py` – A Kafka producer that sends a message to the `purchases` topic.

## Requirements

- Python 3.6+
- Kafka (running locally or accessible at the configured bootstrap server)
- `confluent-kafka` Python library

Install dependencies:

```bash
pip install confluent-kafka

Configuration
localhost:57891
