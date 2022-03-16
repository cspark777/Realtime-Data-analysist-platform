from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.conf import settings
from django.core import serializers

from random import uniform
from kafka import KafkaProducer
import time
import json
import datetime
import uuid
from simulations.models import Simulation

bootstrap_server = settings.KAFKA_URL
producer = None


def send_kafka_message(topic, message):
    global bootstrap_server, producer
    if bootstrap_server and not producer:
        producer = KafkaProducer(bootstrap_servers=bootstrap_server)
    if not bootstrap_server:
        print('No Brokers Available')
        return
    print("Sending KAFKA message")
    print(topic)
    print(message)
    message = json.loads(message)
    # Insert timestamp if not already specified
    if 'timestamp' not in message: 
        message['timestamp'] = datetime.datetime.now().isoformat()

    # Insert uuid if not already specified
    if 'uuid' not in message:
        message['uuid'] = str(uuid.uuid4())

    message = json.dumps(message)
    producer.send(topic, message.encode('utf-8'))
    producer.flush()
    print("SENT message")


def run_simulation(request, project_id, simulation_id):
    simulation = Simulation.objects.filter(pk=simulation_id, created_by=request.user, project_id=project_id)
    if simulation.exists():
        simulation = simulation.first()
        steps = simulation.step_set.order_by('ordering')
        dsl = {'simulation_metrics': {
            'run_type': simulation.run_type,
            'run_count': simulation.run_count,
            'run_time': simulation.run_time,
        }}
        steps_data = json.loads(serializers.serialize('json', steps))
        steps_data = list(map(lambda i: i.get('fields'), steps_data))
        dsl['steps'] = steps_data
        dsl = json.dumps(dsl)
        for step in steps:
            delay = step.static_value if step.delay_type == 'static' else uniform(0, step.random_value)
            if delay:
                print(step.description)
                time.sleep(delay)
            send_kafka_message(topic=step.topic, message=step.event)
    else:
        print('Simulation does not exist.')

    return HttpResponseRedirect(reverse_lazy('projects:simulations:simulations_list',
                                             kwargs={'project_id': project_id}))
