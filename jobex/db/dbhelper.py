import psycopg2
import logging
from jobex.strana import key_words
from jobex.twitter.tweet import Tweet
from jobex.twitter.tweet_job_analysis import TweetAnalysisResult
import uuid

logger = logging.getLogger(__name__)

def insert_tweet(tweet : Tweet, is_job_tweet : bool, result : TweetAnalysisResult):
    keywords = ",".join(result.tech_keywords) if len(result.tech_keywords) > 0 else ""
    url = ""
    if len(tweet.urls) > 0:
        if tweet.urls[0].expanded_url and len(tweet.urls[0].expanded_url.strip()) > 0:
            url = tweet.urls[0].expanded_url
        else:
            url = tweet.urls[0].url
    id = str(uuid.uuid4())
    query = f'''INSERT INTO public.lt_jobtweet
                (id, tweet_id, value, "text", author_id, createddatetimeutc, isjobtweet, keywords, url1, url2, url3, url4, url5)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
    con = create_connection("twitterjobdb", "postgres", "postgres", "localhost", "5432")
    execute_query(con, query, (id, tweet.tweet_id, tweet.payload, tweet.text, tweet.author_id, tweet.created_at, is_job_tweet, keywords, url, "", "", "", ""))
    return id

def insert_page(page_content, keywords, url, tweet_source_id, error_text):
    keywords = ",".join(keywords) if len(keywords) > 0 else ""
    id = str(uuid.uuid4())
    query = f'''INSERT INTO public.lt_jobpage
                (id, pagecontent, keywords, url, errortext, tweetsourceid)
                VALUES(%s, %s, %s, %s, %s, %s);
            '''
    con = create_connection("twitterjobdb", "postgres", "postgres", "localhost", "5432")
    execute_query(con, query, (id, page_content, keywords, url, error_text, tweet_source_id))
    return id

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        logger.info("Connection to PostgreSQL DB successful")
    except BaseException as e:
        logger.error(f"dbhelper create connection: The error '{e}' occurred")
        raise e
    return connection

def execute_query(connection, query, args):
    connection.autocommit = True    
    try:
        cursor = connection.cursor()
        cursor.execute(query, args)
    except BaseException as e:
        logger.error(f"dbhelper execute query: The error '{e}' occurred")
        raise e

def execute_read_query(connection, query):
    result = None
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except BaseException as e:
        logger.error(f"dbhelper execute read query: The error '{e}' occurred")
        raise e


