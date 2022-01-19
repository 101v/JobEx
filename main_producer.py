import logging
import threading
from jobex.kafka.consumer import KafkaConsumer
from jobex.kafka.producer import KafkaProducer
from jobex.db import dbhelper
from jobex.twitter.tweet import Tweet
import kafka_config
import jobex.twitter.rules as rules
import jobex.twitter.twit_streamer_with_retry as streamer
import jobex.twitter.tweet_job_analysis as tweet_analysis
from init_logger import init_logger
from jobex.webpage import webpage_extraction

init_logger()
logger = logging.getLogger(__name__)

# Prepare Kafka producer
# TODO: Pending to create new producer on kafka error
logger.info("Kafka producer init started")
kafka_producer = KafkaProducer(
    kafka_config.server_endpoint,
    topic="jobex-twitter-job-tweets-v1")
kafka_producer.init_producer()
logger.info("Kafka producer init completed")

# callback to call on arrival of new tweet
def on_data(data):
    if isinstance(data, str):
        kafka_producer.produce("tweet", data)
    print(data)
    print("=================================================")
    print("")

# Check filter rules and update them if required
rules.commit_filter_rules_if_required()

# Start streamer on new thread
streamer_thrd = threading.Thread(target=streamer.start, args=(on_data, ))
streamer_thrd.start()
logger.info("streamer thread started")

choice = ''
while choice != 'q' and choice != 'Q':
    choice = input("Press q/Q to exit")

logger.info("Terminating the application")
streamer.stop()
streamer_thrd.join()
logger.info("Streamer stopped")
kafka_producer.complete()
logger.info("kafka producer completed")
logger.info("Termination completed")