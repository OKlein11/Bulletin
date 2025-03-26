import dateutil
import requests
from typing import Callable
import feedparser
from .helpers import get_template
import markdown


DEFAULT_TEMPLATE_FOLDER = "templates"

class Section:
    default_template:str = "section.html"
    def __init__(self,
                 process_function:Callable,
                 config={},
                 template:str = None,
                 template_folder:str=DEFAULT_TEMPLATE_FOLDER,
                 ):
        self.process_function = process_function
        self.config = config
        self.template_folder = template_folder
        if template is not None:
            self.template = template


    def _process(self
                 ):
        return self.process_function(self.config)



    def render(self):
        data = self._process()

        template = get_template(self)
        return template.render(data=data)
    
    

class IndividualRSSFeed(Section):
    default_template = "individual_rss.html"
    def __init__(self,
                 url:str, 
                 config={
                     "items":5,
                     "since_last":False
                     }, 
                 template:str = None,
                 template_folder:str = DEFAULT_TEMPLATE_FOLDER):
        conf = config
        conf["url"] = url
        super().__init__(self._process_rss_feed, 
                         conf, 
                         template=template,
                         template_folder=template_folder)



    @staticmethod
    def _process_rss_feed(config:dict):
        parsed_feed: feedparser.FeedParserDict = feedparser.parse(config["url"])
        data = {}
        data["title"] = parsed_feed.feed.title
        data["items"] = []
        items = min(config["items"], len(parsed_feed.entries))
        for item in range(items):
            i = {}
            i["href"] = parsed_feed.entries[item].link
            i["pub_date"] = dateutil.parser.parse(parsed_feed.entries[item].published)
            i["title"] = parsed_feed.entries[item].title
            data["items"].append(i)
        return data


class RequestsGetSection(Section):
    def __init__(self,
                 url:str,
                 headers:str={},
                 return_type:str="json",
                 params:dict = {},
                 config={}, 
                 template = None, 
                 template_folder = DEFAULT_TEMPLATE_FOLDER):
        config["url"] = url
        config["headers"] = headers
        config["return_type"] = return_type
        config["params"] = params
        super().__init__(self._process_request_get, config, template, template_folder)

    @staticmethod
    def _process_request_get(config:dict) -> dict | str:
        url = config["url"]
        req = requests.get(url, headers=config["headers"],params=config["params"])
        try:
            assert req.status_code == 200
        except AssertionError as e:
            raise ValueError(f"Request to {url} Failed")
        if config["return_type"] == "json":
            return req.json()
        elif config["return_type"] == "text":
            return req.content.decode()

    
class PlainTextSection(Section):
    default_template = "plain_text_section.html"
    def __init__(self, 
                 text:str,
                 encoding:str="html", 
                 config={}, 
                 template = None, 
                 template_folder = DEFAULT_TEMPLATE_FOLDER):
        config["text"] = text
        config["encoding"] = encoding
        super().__init__(
                        process_function=self._process_plain_text, 
                        config=config, 
                        template=template, 
                        template_folder=template_folder)
    
    @staticmethod
    def _process_plain_text(config) -> str:
        if config["encoding"] == "html":
            return config["text"]
        elif config["encoding"] == "markdown":
            return markdown.markdown(config["text"])

