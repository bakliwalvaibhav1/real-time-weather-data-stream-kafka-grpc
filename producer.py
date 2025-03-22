import time
from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
from kafka.errors import UnknownTopicOrPartitionError, TopicAlreadyExistsError
import weather
from report_pb2 import Report

broker = 'localhost:9092'
admin_client = KafkaAdminClient(bootstrap_servers=[broker])
print(admin_client.describe_topics(["temperatures"]))

try:
    admin_client.delete_topics(["temperatures"])
    print("Deleted topics successfully")
except UnknownTopicOrPartitionError:
    print("Cannot delete topic/s (may not exist yet)")


time.sleep(3) # Deletion sometimes takes a while to reflect

producer = KafkaProducer(bootstrap_servers=[broker], retries=10, acks="all")

# Create topic 'temperatures' with 4 partitions and replication factor = 1
try:
    admin_client.create_topics([NewTopic("temperatures", num_partitions=4, replication_factor=1)])
except TopicAlreadyExistsError:
    print("temperatures already exist")

for date, degrees, station_id in weather.get_next_weather(delay_sec=0.1):
    value = Report(date=date, degrees=degrees, station_id=station_id).SerializeToString()
    key = bytes(station_id, "utf-8")
    producer.send(topic="temperatures", value=value, key=key)
    
print("Topics:", admin_client.list_topics())
