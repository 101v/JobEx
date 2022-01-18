import jobex.twitter.tweet_job_analysis as tana
from jobex.webpage import webpage_extraction

# payload = ""
# with open("testtweet.txt") as f:
#     payload = f.read()
# tweet = tana.Tweet(payload)
# result = tana.analyze_tweet(tweet)
# is_job_tweet = tana.is_tech_job_tweet(result)
# print(is_job_tweet)

webpage_extraction.analyze_webpage("https://www.linkedin.com/jobs/view/2862258723", "1234")