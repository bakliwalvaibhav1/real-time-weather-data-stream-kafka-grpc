from kafka import KafkaConsumer, TopicPartition
from report_pb2 import Report
import json
import os
import sys

broker = "localhost:9092"
consumer = KafkaConsumer(bootstrap_servers=[broker])

partitions = [int(p) for p in sys.argv[1:]]  # Convert arguments to integers
consumer.assign([TopicPartition("temperatures", p) for p in partitions])

# Ensure data directory exists
data_dir = "./data"
os.makedirs(data_dir, exist_ok=True)

# Initialize partition files
json_report = {"offset": 0}
for part in partitions:
    file_path = f"{data_dir}/partition-{part}.json"
    
    if not os.path.exists(file_path):
        with open(file_path, "w") as outfile:
            json.dump(json_report, outfile, indent=4)
    else:
        with open(file_path) as json_file:
            json_report = json.load(json_file)
        consumer.seek(TopicPartition("temperatures", part), json_report["offset"])

while True:
    batch = consumer.poll(1000)
    if not batch:
        continue  # Avoid unnecessary processing if no messages arrive

    for tp, messages in batch.items():
        part = tp.partition  # Correct way to get partition number

        with open(f"{data_dir}/partition-{part}.json") as json_file:
            json_report = json.load(json_file)

        for msg in messages:
            report = Report.FromString(msg.value)

            json_report.setdefault(report.station_id, {"count": 0, "sum": 0, "start": report.date})
            json_report[report.station_id]["count"] += 1
            json_report[report.station_id]["sum"] += report.degrees
            json_report[report.station_id]["avg"] = json_report[report.station_id]["sum"] / json_report[report.station_id]["count"]
            json_report[report.station_id]["end"] = report.date
            json_report["offset"] = consumer.position(tp)

            print(json_report)

        # Save the updated report
        with open(f"{data_dir}/partition-{part}.json.tmp", "w") as outfile:
            json.dump(json_report, outfile, indent=4)
        os.rename(f"{data_dir}/partition-{part}.json.tmp", f"{data_dir}/partition-{part}.json")
