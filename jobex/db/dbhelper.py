import psycopg2
import logging
from jobex.strana import key_words
from jobex.twitter.tweet import Tweet
from jobex.twitter.tweet_job_analysis import TweetAnalysisResult
import uuid
import jobex.webpage

logger = logging.getLogger(__name__)

def insert_tweet(tweet : Tweet, is_job_tweet : bool, result : TweetAnalysisResult):
    tweet.payload = tweet.payload.replace("\'", "''")
    tweet.text = tweet.text.replace("\'", "''")
    keywords = ",".join(result.tech_keywords) if len(result.tech_keywords) > 0 else ""
    url1 = tweet.urls[0].url if len(tweet.urls) > 0 else ""
    url2 = tweet.urls[1].url if len(tweet.urls) > 1 else ""
    url3 = tweet.urls[2].url if len(tweet.urls) > 2 else ""
    url4 = tweet.urls[3].url if len(tweet.urls) > 3 else ""
    url5 = tweet.urls[4].url if len(tweet.urls) > 4 else ""
    is_job_tweet = 1 if is_job_tweet else 0
    id = str(uuid.uuid4())
    query = f'''INSERT INTO public.lt_jobtweet
                (id, tweet_id, value, "text", author_id, createddatetimeutc, isjobtweet, keywords, url1, url2, url3, url4, url5)
                VALUES('{id}', '{tweet.tweet_id}', '{tweet.payload}', '{tweet.text}', '{tweet.author_id}', '{tweet.created_at}', '{is_job_tweet}', '{keywords}', '{url1}', '{url2}', '{url3}', '{url4}', '{url5}')
            '''
    con = create_connection("twitterjobdb", "postgres", "postgres", "localhost", "5432")
    execute_query(con, query)
    return id

def insert_page(page_content, keywords, url, tweet_source_id, error_text):

    page_content = page_content.replace("\'", "''")
    keywords = ",".join(keywords) if len(keywords) > 0 else ""
    id = str(uuid.uuid4())
    query = f'''INSERT INTO public.lt_jobpage
                (id, pagecontent, keywords, url, errortext, tweetsourceid)
                VALUES('{id}', '{page_content}', '{keywords}', '{url}', '{error_text}', '{tweet_source_id}');
            '''
    con = create_connection("twitterjobdb", "postgres", "postgres", "localhost", "5432")
    execute_query(con, query)
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

def execute_query(connection, query):
    connection.autocommit = True    
    try:
        cursor = connection.cursor()
        cursor.execute(query)
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


