import dateutil
import requests
from typing import Callable
import feedparser
from .helpers import get_template
import markdown


DEFAULT_TEMPLATE_FOLDER = "templates"

class Section:
    """
    The parent class of all section classes. Creates a section that can be added to a bulletin

    Attributes
    -----
    default_template : str
        The default template for this section, stored in Bulletin's files.

        This value is set at a class level

        For this class the default is 'section.html'
    process_fuction : Callable
        This is the function the section will use when processing. 

        Should be a function that takes a dictionary as input, then returns in a format that is processable by the render method and template
    config : dict
        Any data needed for the process_function, or other objects should be stored here. Any information needed that is not directly for the Section class' functions should be stored here
    template_folder : str
        The path relative to the current working directory where a non-default template is stored.

        If no path is given, will return None
    template : str, optional
        The name of a template file within the template_folder directory. Will be used in place of the default template

        This attribute will only exist if a template is given on initialization of the object

    Methods
    -------
    render()
        Processes according to the process_fuction, then renders the object into the given Jinja template


    Default Template
    -----
        {{ data }}
    """

    
    default_template:str = "section.html"
    def __init__(self,
                 process_function:Callable,
                 config:dict={},
                 template:str = None,
                 template_folder:str=DEFAULT_TEMPLATE_FOLDER,
                 ) -> None:
        """
        Parameters
        -------
        process_fuction : Callable
            This is the function the section will use when processing. 

            Should be a function that takes a dictionary as input, then returns in a format that is processable by the render method and template
        config : dict, optional
            Any configuration needed for the process_function.
        template : str, optional
            The name of a template file within the template_folder directory. Will be used in place of the class' default template
        template_folder : str, optional
            The path relative to the current working directory where a non-default template is stored.

        """
        self.process_function = process_function
        self.config = config
        self.template_folder = template_folder
        if template is not None:
            self.template = template


    def _process(self
                 ) -> any:
        """
        Runs the process_function by passing the object's config

        Should not be run by the user. 

        Returns 
        -----
        Any 
            the output of the process_function
        """
        return self.process_function(self.config) 



    def render(self) -> str:
        """
        Processes the object using _process, then gets the Jinja template for the object and renders it using the data from the process function

        Returns
        -----
        str
            the str of html from the rendered Jinja template
        """
        data = self._process()

        template = get_template(self)
        return template.render(data=data)
    
    

class IndividualRSSFeed(Section):
    """
    A section class that returns the contents of an RSS feed at the given url

    Attributes
    -----
    default_template : str
        The default template for this section, stored in Bulletin's files.

        This value is set at a class level

        For this class the default is 'individual_rss.html'
    config : dict
        Stores configuration information for this section

        See 'Config Option' for what values can be used for this object
    template_folder : str
        The path relative to the current working directory where a non-default template is stored.

        If no path is given, will return None
    template : str, optional
        The name of a template file within the template_folder directory. Will be used in place of the default template

        This attribute will only exist if a template is given on initialization of the object

    Methods
    -------
    render()
        Processes according to the process_fuction, then renders the object into the given Jinja template



    Config Options
    -----
    items : int
        The number of items that should be returned from the rss feed. If there are fewer items available than this number, the maximum number will be returned

        Default is 5.
    since_last : bool
        NOT IMPLEMENTED
    url : str
        The url of the rss feed
    
    Default Template
    -----
        {{ RSS Feed Title }}
        list({{ Item Hyperlink }} ({{ Item Name }}))
    """
    default_template = "individual_rss.html"
    def __init__(self,
                 url:str, 
                 config: dict={
                     "items":5,
                     "since_last":False
                     }, 
                 template:str = None,
                 template_folder:str = DEFAULT_TEMPLATE_FOLDER) -> None:
        """
        Parameters
        -------
        url : str 
            The URL of the rss to be used
        config : dict, optional
            The configuration for the section.

            Default: {"items":5, "since_last":False}
        template : str, optional
            The name of a template file within the template_folder directory. Will be used in place of the class' default template
        template_folder : str, optional
            The path relative to the current working directory where a non-default template is stored.

        """
        conf = config
        conf["url"] = url
        super().__init__(self._process_rss_feed, 
                         conf, 
                         template=template,
                         template_folder=template_folder)



    @staticmethod
    def _process_rss_feed(config:dict) -> dict:
        """
        The process_function for Individual RSS Feeds. takes in the config and returns a dict with all the data

        Parameters
        -----
        config : dict
            The config of the section

        Returns
        -----
        dict
            A dict containing the title of the feed. Along with items that have title, pub_date, and href link
        """

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
    """
    A section class that pulls data from a website using a get call

    Attributes
    -----
    default_template : str
        The default template for this section, stored in Bulletin's files.

        This value is set at a class level

        For this class the default is 'section.html'
    config : dict
        Any config needed for the section
    template_folder : str
        The path relative to the current working directory where a non-default template is stored.

        If no path is given, will return None
    template : str, optional
        The name of a template file within the template_folder directory. Will be used in place of the default template

        This attribute will only exist if a template is given on initialization of the object

    Methods
    -------
    render()
        Processes according to the process_fuction, then renders the object into the given Jinja template


    Default Template
    -----
        {{ data }}
    """
    
    def __init__(self,
                 url:str,
                 headers:str={},
                 return_type:str="json",
                 params:dict = {},
                 config={}, 
                 template = None, 
                 template_folder = DEFAULT_TEMPLATE_FOLDER) -> None:
        """
        Parameters
        -------
        url : str 
            The URL of the site to pull from
        headers : dict, optional
            Any headers to pass to the request
        return_type : str, optional
            What type to return as.

            Allowed values: ["json","text"]

            Default: "json"
        params : dict
            Any additional params to pass to the request
        config : dict, optional
            The configuration for the section.

            Default: {}
        template : str, optional
            The name of a template file within the template_folder directory. Will be used in place of the class' default template
        template_folder : str, optional
            The path relative to the current working directory where a non-default template is stored.

        """
        config["url"] = url
        config["headers"] = headers
        config["return_type"] = return_type
        config["params"] = params
        super().__init__(self._process_request_get, config, template, template_folder)

    @staticmethod
    def _process_request_get(config:dict) -> dict | str:
        """
        Runs a get request from the url assigned. Returns data either as processed json or plain text

        Parameters
        -----
        config : dict
            the configuration of the request
        
        Returns
        -----
        dict
            Returns the value of the get request jsonified. determined by the config's "return_type" value
        str
            Returns the value of the get request as plain text. determined by the config's "return_type" value
        """
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
    """
    A section class that renders plain text given

    Attributes
    -----
    default_template : str
        The default template for this section, stored in Bulletin's files.

        This value is set at a class level

        For this class the default is 'plain_text_section.html'
    config : dict
        Configuration for this section
    template_folder : str
        The path relative to the current working directory where a non-default template is stored.

        If no path is given, will return None
    template : str, optional
        The name of a template file within the template_folder directory. Will be used in place of the default template

        This attribute will only exist if a template is given on initialization of the object

    Methods
    -------
    render()
        Processes according to the process_fuction, then renders the object into the given Jinja template


    Default Template
    -----
        {{ data }}
    """
    default_template = "plain_text_section.html"
    def __init__(self, 
                 text:str,
                 encoding:str="html", 
                 config={}, 
                 template = None, 
                 template_folder = DEFAULT_TEMPLATE_FOLDER) -> None:
        """
        Parameters
        -------
        text : str
            The text to be rendered in the template
        encoding : str, optional
            The encoding of the text. Options are html and markdown. Default html

            Markdown will be rendered according to the markdown syntax

            html will be rendered as raw html
        config : dict, optional
            Any configuration.
        template : str, optional
            The name of a template file within the template_folder directory. Will be used in place of the class' default template
        template_folder : str, optional
            The path relative to the current working directory where a non-default template is stored.

        """
        config["text"] = text
        config["encoding"] = encoding
        super().__init__(
                        process_function=self._process_plain_text, 
                        config=config, 
                        template=template, 
                        template_folder=template_folder)
    
    @staticmethod
    def _process_plain_text(config) -> str:
        """
        Renders the config to a str to be passed to the render function

        Parameters
        -----
        config : dict
            The config required to render
        """
        if config["encoding"] == "html":
            return config["text"]
        elif config["encoding"] == "markdown":
            return markdown.markdown(config["text"])

