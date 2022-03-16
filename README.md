

# How to setup your development environment

- Download latest APACHE KAFKA
- Download latest APACHE DRUID 
- Download latest APACHE ZOOKEEPER

pip install -r requirements.txt

# Capture IP Address

- export MY_IP=192.168.0.8 (Subtitute your IP Address) 

# Run ZOOKEEPEER

- Command TBC

# Run Postgres

- Command TBC


# Run DRUID

- ./bin/start-single-server-small.sh

# Run KAFKA

- bin/kafka-server-start.sh config/server.properties --override advertised.listeners=PLAINTEXT://$MY_IP:9092


# Testine environment health 

- Confirm Kafka logs are healthy 
- Open source tool Conduktor can be used to browse GUI 
- Visit localhost 8888 to see Druid GUI 

# Running the DATA-admin-gui

## Best to run outside of Docker for now....

- export MY_IP=192.168.0.8 
- export DATA_SERVER=http://0.0.0.0:5000/
- export DRUID_URL=$MY_IP:8888
- export KAFKA_URL=$MY_IP:9092
- python manage.py runserver

# Running the DATA-server

- export MY_IP=192.168.0.8 
- export DRUID_URL=$MY_IP:8888
- export KAFKA_URL=$MY_IP:9092
- python server.py -h 0.0.0.0

# Using app 

- Gui should be available on localhost port 80 
