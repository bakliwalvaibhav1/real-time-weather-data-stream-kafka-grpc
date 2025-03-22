python3 -m venv venv
source venv/bin/activate
pip install kafka-python grpcio grpcio-tools


python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. report.proto

zookeeper-server-start /opt/homebrew/etc/kafka/zookeeper.properties

kafka-server-start /opt/homebrew/etc/kafka/server.properties

