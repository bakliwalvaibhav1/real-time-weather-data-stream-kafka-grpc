from kafka import KafkaConsumer
from kafka import TopicPartition
from report_pb2 import Report

broker = "localhost:9092"
consumer = KafkaConsumer(bootstrap_servers=[broker])
consumer.subscribe(["temperatures"])
# print(consumer.assignment())
# print(consumer.partitions_for_topic("temperatures"))
while True:
    batch = consumer.poll(1000)
    for tp, messages in batch.items():
        for msg in messages:
            msg = Report.FromString(msg.value)
            weather_dict = {}
            weather_dict['station_id'] = msg.station_id
            weather_dict['date'] = msg.date
            weather_dict['degrees'] = msg.degrees
            weather_dict['partition'] = tp[1]
            print(weather_dict)
