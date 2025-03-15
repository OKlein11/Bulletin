from .section import Section
import feedparser
import datetime
from time import mktime

class IndividualRSSFeed(Section):
    def __init__(self,link:str, template = "individual_rss.html", config={"items":5,"since_last":False}):
        conf = config
        conf["link"] = link
        super().__init__(self._process_rss_feed, template, conf)



    @staticmethod
    def _process_rss_feed(config:dict):
        parsed_feed: feedparser.FeedParserDict = feedparser.parse(config["link"])
        data = {}
        data["title"] = parsed_feed.feed.title
        data["items"] = []
        items = min(config["items"], len(parsed_feed.entries))
        for item in range(items):
            i = {}
            i["href"] = parsed_feed.entries[item].link
            i["pub_date"] = datetime.datetime.fromtimestamp(mktime((parsed_feed.entries[item].published_parsed)))
            i["title"] = parsed_feed.entries[item].title
            data["items"].append(i)
        return data