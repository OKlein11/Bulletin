import dateutil
import jinja2
import inspect
import os
from typing import Callable
import feedparser

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

        if hasattr(self,"template"):
            template = self.template
            folder = self.template_folder
        else:
            template = self.__class__.default_template
            folder = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), "templates")


        template_loader = jinja2.FileSystemLoader(searchpath= folder)


        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template)
        return template.render(data=data)
    
    

class IndividualRSSFeed(Section):
    default_template = "individual_rss.html"
    def __init__(self,
                 link:str, 
                 config={
                     "items":5,
                     "since_last":False
                     }, 
                 template:str = None,
                 template_folder:str = DEFAULT_TEMPLATE_FOLDER):
        conf = config
        conf["link"] = link
        super().__init__(self._process_rss_feed, 
                         conf, 
                         template=template,
                         template_folder=template_folder)



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
            i["pub_date"] = dateutil.parser.parse(parsed_feed.entries[item].published)
            i["title"] = parsed_feed.entries[item].title
            data["items"].append(i)
        return data