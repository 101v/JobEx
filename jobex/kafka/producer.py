from confluent_kafka import Producer
import logging

logger = logging.getLogger(__name__)


class KafkaProducer:
    def __init__(self, server_endpoint, topic) -> None:
        self.server_endpoint = server_endpoint
        self.topic = topic
        self.producer = None

    def init_producer(self):
        kafka_conf = {'bootstrap.servers': self.server_endpoint}
        self.producer = Producer(kafka_conf)
        logger.info("Kafka producer initialized")

    def _acked(err, msg):
        if err is not None:
            logger.critical("Failed to deliver message: {0} : {1}".format(
                    msg.value(),
                    err.str()
                )
            )
        # TODO: test that, should we throw error from here to retry?

    def produce(self, key, value):
        self.producer.produce(
            self.topic,
            key=key,
            value=value,
            callback=KafkaProducer._acked)
        self.producer.poll(0.5)

    def complete(self):
        self.producer.flush()
        logger.info("Kafka producer flushed")
