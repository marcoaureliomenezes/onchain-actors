import os
from kafka import KafkaConsumer
import logging
from subprocess import Popen

logging.basicConfig(level='INFO')

def run_concurrently(commands_list):
    procs = [ Popen(i) for i in commands_list ]
    for p in procs:
        p.wait()
    return


def get_kafka_consumer(topic, group_id, auto_offset_reset='latest'):
    host = os.environ['KAFKA_HOST'].split(",")
    return KafkaConsumer(topic, bootstrap_servers=host,
                        auto_offset_reset=auto_offset_reset, group_id=group_id)


if __name__ == '__main__':
    topic_listened = os.environ["TOPIC_EXECUTORS"]
    consumer_group = os.environ["CONSUMER_GROUP"]
    onchain_actor_consumer = get_kafka_consumer(topic_listened, consumer_group)
    for msg in onchain_actor_consumer:
        command = [msg.value.decode('utf-8').replace('"',  "").split(" ")]
        run_concurrently(command)
