<h1 align="center">Real-Time Weather Data Stream with Kafka and gRPC</h3>

This project demonstrates the real-time processing of weather data using **Apache Kafka** for stream processing and **gRPC** for efficient communication. It consists of a **Producer** that generates weather data and sends it to Kafka topics, and a **Consumer** that processes the data and computes statistics.

## Table of Contents
- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Running the Project](#running-the-project)
  - [Kafka Setup](#kafka-setup)
  - [Producer](#producer)
  - [Consumer](#consumer)
- [Directory Structure](#directory-structure)

## Overview
In this project, weather data (temperature, station ID, and date) is produced and sent to Kafka topics, partitioned across multiple partitions. The **Producer** generates data and publishes it to the `temperatures` topic in Kafka, while the **Consumer** listens to specific partitions of this topic, processes the data, and computes basic statistics like average temperature per station.

- **Producer**: Sends weather reports to Kafka.
- **Consumer**: Reads weather reports, calculates statistics, and stores results in JSON files.
- **Kafka**: Used as a message broker for reliable data streaming.
- **gRPC**: Used for efficient communication and serialization of messages.
- **Protobuf**: For defining the structure of messages exchanged between Producer and Consumer.
- **JSON**: Used for storing and handling data for statistics calculation.

## Technologies Used

<p align="center">
  <a href="https://go-skill-icons.vercel.app/">
    <img src="https://go-skill-icons.vercel.app/api/icons?i=kafka,python,grpc,json" />
  </a>
</p>

| Technology | Description |
|------------|-------------|
| Kafka      | A distributed event streaming platform. |
| Python     | The programming language used for both the Producer and Consumer. |
| gRPC       | Used for efficient communication and serialization of messages. |
| Protobuf   | For defining the structure of messages exchanged between Producer and Consumer. |
| JSON       | Used for storing and handling data for statistics calculation. |


## Getting Started
Follow the steps below to get the project running on your local machine.

### Prerequisites
1. **Kafka**: You need to have **Apache Kafka** running locally. Follow the [Kafka Installation Guide](https://kafka.apache.org/quickstart) to set up Kafka on your machine.

2. **Python 3.x**: Ensure Python 3 and `pip` are installed on your system.

3. **Install Kafka Python Client**:  
   Install the Kafka Python client using the following command:

   ```bash
   pip install kafka-python
   ```

4. **Install gRPC & Protobuf**:  
   To install gRPC and Protobuf libraries:

   ```bash
   pip install grpcio grpcio-tools
   ```

### Running the Project

#### Kafka Setup
1. **Start Zookeeper**:
   
   ```bash
   zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties
   ```

2. **Start Kafka Broker**:

   ```bash
   kafka-server-start /usr/local/etc/kafka/server.properties
   ```

3. **Create a Kafka Topic**:
   Run the following command to create the `temperatures` topic with 4 partitions:

   ```bash
   kafka-topics --bootstrap-server localhost:9092 --create --topic temperatures --partitions 4 --replication-factor 1
   ```

#### Producer
The **Producer** generates weather data and sends it to Kafka.

1. **Run the Producer**:

    ```bash
    python producer.py
    ```

   The Producer will continuously generate weather data and send it to Kafka, using the `station_id` as the key to ensure that messages are distributed across the partitions.

#### Consumer
The **Consumer** reads the weather data from Kafka partitions, processes it, and calculates statistics such as the average temperature for each station.

1. **Run the Consumer**:

   ```bash
   python consumer.py <partition_number_1> <partition_number_2> ...
   ```

   Replace `<partition_number_1>`, `<partition_number_2>`, etc., with the partitions you wish the consumer to read from (e.g., `0 1`).

2. **Output**:
   The Consumer will output processed statistics and save them into JSON files (`partition-0.json`, `partition-1.json`, etc.) located in the `./data` folder.

## Directory Structure
```bash
├── data/                    # Folder containing JSON files for partition statistics
│   ├── partition-0.json
│   ├── partition-1.json
│   └── ...
├── README.md                # Project documentation
├── consumer.py              # Consumer script to process Kafka messages
├── debug.py                 # Debug script to check Kafka stream
├── producer.py              # Producer script to send data to Kafka
├── report.proto             # Proto file with weather data structure
├── report_pb2.py            # Script generated using proto file
├── report_pb2_grpc.py       # gRPC Protobuf file for weather data structure
└── weather.py               # Script to produce weather data
```
