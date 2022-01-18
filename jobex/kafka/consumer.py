from confluent_kafka import Consumer, KafkaError, KafkaException
import logging

logger = logging.getLogger(__name__)

class KafkaConsumer:
    def __init__(self, server_endpoint, group, topic, on_receive) -> None:
        self.server_endpoint = server_endpoint
        self.group = group
        self.topic = topic
        self.consumer = None
        self.msg_count = 0
        self.min_commit_count = 10
        self.on_receive = on_receive
        self.running = False

    def init_consumer(self):
        kafka_conf = {'bootstrap.servers': self.server_endpoint,
        'group.id': self.group,
        'enable.auto.commit': False,
        'auto.offset.reset': 'smallest'}

        self.consumer = Consumer(kafka_conf)
        self.consumer.subscribe([self.topic])
        logger.info("Kafka consumer initialized")

    def start(self):
        self.running = True
        try:

            while self.running:
                msg = self.consumer.poll(timeout=5.0)
                if msg is None: 
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        logger.info('%% %s [%d] kafka consumer reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    self.on_receive(msg)
                    self.msg_count += 1
                    if self.msg_count % self.min_commit_count == 0:
                        self.consumer.commit(asynchronous=False)
        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()

    def stop(self):
        self.running = False