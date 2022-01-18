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

# callback to call on receiving message from Kafka consumer
def on_meg(data):
    msg = data.value()
    if msg:
        msg = msg.decode("utf-8")
        tweet = Tweet(msg)
        result = tweet_analysis.analyze_tweet(tweet)
        is_job_tweet = tweet_analysis.is_tech_job_tweet(result)
        id = dbhelper.insert_tweet(tweet, is_job_tweet, result)
        if len(tweet.urls) > 0 and is_job_tweet:
            webpage_extraction.analyze_webpage(tweet.urls[0].url, id)


# Prepare Kafka consumer
# TODO: Pending to create new consumer on kafka error
logger.info("Kafka consumer init started")
kafka_consumer = KafkaConsumer(
    kafka_config.server_endpoint,
    "job-tweet-group",
    "jobex-twitter-job-tweets-v1",
    on_meg
)
kafka_consumer.init_consumer()
logger.info("Kafka consumer init completed")

# Check filter rules and update them if required
rules.commit_filter_rules_if_required()

# Start streamer on new thread
streamer_thrd = threading.Thread(target=streamer.start, args=(on_data, ))
streamer_thrd.start()
logger.info("streamer thread started")

# Start kafka consumer on new thread
consumer_thrd = threading.Thread(target=kafka_consumer.start)
consumer_thrd.start()
logger.info("kafka consumer thread started")

choice = ''
while choice != 'q' and choice != 'Q':
    choice = input("Press q/Q to exit")

logger.info("Terminating the application")
streamer.stop()
streamer_thrd.join()
logger.info("Streamer stopped")
kafka_producer.complete()
logger.info("kafka producer completed")
kafka_consumer.stop()
consumer_thrd.join()
logger.info("kafka consumer stopped")

logger.info("Termination completed")