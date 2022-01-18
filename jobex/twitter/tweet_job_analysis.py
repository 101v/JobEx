from jobex.twitter.tweet import Tweet
from jobex.strana import simple_match, key_words

def is_tech_job_tweet(result):
    if result and len(result.tech_keywords) > 0:
        if len(result.hiring_words) > 0 or len(result.hiring_hashtags) > 0:
            return True
    return False

def analyze_tweet(tweet: Tweet):
    matched_hiring_words = match_hiring_words(tweet)
    matched_hashtags = match_hiring_hashtags(tweet)
    matched_tech_keywords = match_tech_keywords(tweet)
    return TweetAnalysisResult(matched_hiring_words, matched_hashtags, matched_tech_keywords)

def match_hiring_words(tweet: Tweet):
    tokens = simple_match.tokenize(tweet.text_without_hashtags)
    return simple_match.find_matches(tokens, key_words.hiring_word_candidates)

def match_hiring_hashtags(tweet: Tweet):
    return simple_match.find_matches(tweet.hashtags, key_words.hiring_hashtag_candidates)

def match_tech_keywords(tweet: Tweet):
    tokens = simple_match.tokenize(tweet.text)
    return simple_match.find_matches(tokens, key_words.tech_keywords_candidates)

class TweetAnalysisResult:
    def __init__(self, hiring_words, hiring_hashtags, tech_keywords) -> None:
        self.hiring_words = hiring_words
        self.hiring_hashtags = hiring_hashtags
        self.tech_keywords = tech_keywords

