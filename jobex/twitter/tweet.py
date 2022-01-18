import json
import types

class Tweet:
    def __init__(self, payload) -> None:
        self.payload = payload
        self._obj = json.loads(payload)
        
        self.tweet_id = None
        self.author_id = None
        self.text = None
        self.text_without_hashtags = None
        self.created_at = None
        self.hashtags = []
        self.urls = []

        self._extract_id()
        self._extract_text()        
        self._extract_hashtags()
        self._extract_urls()
    
    def _extract_id(self):
        self.tweet_id = self._obj["data"]["id"]
        self.author_id = self._obj["data"]["author_id"]

    def _extract_text(self):
        self.text = self._obj["data"]["text"]
        self._extract_text_without_hashtags()
        self.created_at = self._obj["data"]["created_at"]

    def _extract_text_without_hashtags(self):
        hashtags = self._obj["data"].get("entities", {}).get("hashtags", [])
        positions_to_remove = [(hashtag["start"], hashtag["end"]) for hashtag in hashtags]
        if len(positions_to_remove) > 0:
            text = list(self.text)
            positions_to_remove = sorted(positions_to_remove, key=lambda pos: pos[0])
            positions_to_remove.reverse()
            for pos in positions_to_remove:
                del text[pos[0]:pos[1]]
            self.text_without_hashtags = ''.join(text)
        else:
            self.text_without_hashtags = self.text

    def _extract_hashtags(self):
        hashtags = self._obj["data"].get("entities", {}).get("hashtags", [])
        self.hashtags = [hashtag["tag"] for hashtag in hashtags]

    def _extract_urls(self):
        urls = self._obj["data"].get("entities", {}).get("urls", [])
        self.urls = []
        for url in urls:
            tweet_url = types.SimpleNamespace()
            tweet_url.url = url["url"]
            tweet_url.expanded_url = url.get("expanded_url", "")
            tweet_url.unwound_url = url.get("unwound_url", "")
            self.urls.append(tweet_url)

# str = '{"data":{"author_id":"4467848781","created_at":"2022-01-13T05:52:01.000Z","entities":{"mentions":[{"start":0,"end":9,"username":"icanzilb","id":"9596232"}]},"geo":{},"id":"1481504284491411463","source":"Twitter for iPhone","text":"@icanzilb Sounds like a once in a lifetime opportunity 🔥"},"matching_rules":[{"id":"1481504264702898179","tag":"Rule 0"}]}'
# str = '{"data":{"author_id":"21507343","created_at":"2022-01-13T05:54:02.000Z","entities":{"annotations":[{"start":28,"end":37,"probability":0.4075,"type":"Product","normalized_text":"Google Ads"}],"hashtags":[{"start":0,"end":4,"tag":"PPC"}],"urls":[{"start":48,"end":71,"url":"https://t.co/ceIM0LyhtR","expanded_url":"http://dlvr.it/SH26s8","display_url":"dlvr.it/SH26s8","unwound_url":"https://www.reddit.com/r/PPC/comments/s2s0fc/hiring_looking_for_a_google_ads_manager/?utm_source=dlvr.it&utm_medium=twitter"}]},"geo":{},"id":"1481504792622948353","source":"dlvr.it","text":"#PPC (HIRING) Looking for a Google Ads manager. https://t.co/ceIM0LyhtR"},"matching_rules":[{"id":"1481504264702898179","tag":"Rule 0"}]}'
# str = '{"data":{"author_id":"68686173","created_at":"2022-01-04T09:30:37.000Z","entities":{"annotations":[{"start":60,"end":78,"probability":0.4789,"type":"Organization","normalized_text":"Path Safe Programme"}],"hashtags":[{"start":126,"end":131,"tag":"Jobs"},{"start":132,"end":139,"tag":"Hiring"},{"start":140,"end":156,"tag":"ProjectDelivery"},{"start":157,"end":165,"tag":"Science"}],"urls":[{"start":101,"end":124,"url":"https://t.co/497w6y6WCO","expanded_url":"https://www.civilservicejobs.service.gov.uk/csr/index.cgi?SID=Y3NvdXJjZT1jc3FzZWFyY2gmc2VhcmNoX3NsaWNlX2N1cnJlbnQ9MSZwYWdlYWN0aW9uPXZpZXd2YWNieWpvYmxpc3Qmam9ibGlzdF92aWV3X3ZhYz0xNzYzNDc4Jm93bmVyPTUwNzAwMDAmdXNlcnNlYXJjaGNvbnRleHQ9MTQ0NTI4MTc0JnBhZ2VjbGFzcz1Kb2JzJm93bmVydHlwZT1mYWlyJnJlcXNpZz0xNjQwODYzNzY5LTUyZDEwNTI4MjBjZjkyMzk0OGYyOTlhNjE4OGE1NzYzMmY5Y2E0NWU=","display_url":"civilservicejobs.service.gov.uk/csr/index.cgi?…","images":[{"url":"https://pbs.twimg.com/news_img/1478297824286547968/taurwjCb?format=jpg&name=orig","width":1500,"height":1500},{"url":"https://pbs.twimg.com/news_img/1478297824286547968/taurwjCb?format=jpg&name=150x150","width":150,"height":150}],"status":200,"title":"Project Manager - Civil Service Jobs - GOV.UK","description":"Search and apply for opportunities within the Civil Service.","unwound_url":"https://www.civilservicejobs.service.gov.uk/csr/index.cgi?SID=Y3NvdXJjZT1jc3FzZWFyY2gmc2VhcmNoX3NsaWNlX2N1cnJlbnQ9MSZwYWdlYWN0aW9uPXZpZXd2YWNieWpvYmxpc3Qmam9ibGlzdF92aWV3X3ZhYz0xNzYzNDc4Jm93bmVyPTUwNzAwMDAmdXNlcnNlYXJjaGNvbnRleHQ9MTQ0NTI4MTc0JnBhZ2VjbGFzcz1Kb2JzJm93bmVydHlwZT1mYWlyJnJlcXNpZz0xNjQwODYzNzY5LTUyZDEwNTI4MjBjZjkyMzk0OGYyOTlhNjE4OGE1NzYzMmY5Y2E0NWU="},{"start":166,"end":189,"url":"https://t.co/EtC2Wgy5ZU","expanded_url":"https://twitter.com/foodgov/status/1478297809350643712/photo/1","display_url":"pic.twitter.com/EtC2Wgy5ZU"}]},"geo":{},"id":"1478297809350643712","source":"Emplifi","text":"Job Alert: We\'re hiring a Project Manager to help drive the Path Safe Programme forward.\\n\\nApply now: https://t.co/497w6y6WCO\\n\\n#Jobs #Hiring #ProjectDelivery #Science https://t.co/EtC2Wgy5ZU"},"matching_rules":[{"id":"1474322617268011010","tag":"Rule 0"}]}'
# t = Tweet(str)
# print(t.text)
# print(t.text_without_hashtags)
# print(t.hashtags)
# print(t.urls)
