from bulletin.section import *
import pytest
import json
import datetime
import os
from conftest import mock_process_function



@pytest.mark.parametrize(("section_class","kwargs","expected"),[
    (Section,{"process_function":mock_process_function},{"config":{},"template_folder":"templates","default_template":"section.html"}),
    (IndividualRSSFeed,{"url":"http://test.com/feed"},{"config":{"items":5,"since_last":False,"url":"http://test.com/feed"},"default_template":"individual_rss.html"}),
    (RequestsGetSection,{"url":"http://request_get_section_init.com/test"},{"config":{"url":"http://request_get_section_init.com/test","headers":{},"return_type":"json"},"default_template":"section.html"})
])
def test_section_init(section_class:Section,kwargs:dict,expected:dict):
    section = section_class(**kwargs)
    for k,v in expected.items():
        assert getattr(section,k) == v
    if "template" not in kwargs.keys():
        assert not(hasattr(section,"template"))


@pytest.mark.parametrize(("kwargs","section_class","fixtures","expected",),[
     ({"process_function":mock_process_function},Section,[],"section_process.json"),
     ({"url":"http://request_get_section_process.com/test"},RequestsGetSection,["mock_request_get"],"request_get_section_process.json")
])
def test_section_process(kwargs:dict,
                         section_class:Section,
                         fixtures:list,
                         expected:str,
                         request):
    for fixture in fixtures:
        request.getfixturevalue(fixture)
    section = section_class(**kwargs)
    with open(os.path.join("expected",expected)) as f:
        x = json.load(f)
    assert x == section._process()


@pytest.mark.parametrize(("template","template_folder","kwargs","section_class","fixtures","expected"),[
                          (None,None,{"process_function":mock_process_function},Section,[],"section_render_default.txt"),
                          ("section.html",None,{"process_function":mock_process_function},Section,[],"section_render_template.txt"),
                          ("section.html","templates_2",{"process_function":mock_process_function},Section,[],"section_render_template_folder.txt"),
                          (None,"templates_2",{"process_function":mock_process_function},Section,[],"section_render_default.txt"),
                          (None,None,{"url":"http://test_individual_rss.com/feed"},IndividualRSSFeed,["mock_feedparser_parse"],"individual_rss_render_default.txt"),
                          (None,None,{"url":"http://request_get_section_render.com/test"},RequestsGetSection,["mock_request_get"],"request_get_section_render.txt")
                         ])
# Tests the render function. Should be anonymized to work with any Section subclass
# template and template folder are passed to the Section.__init__ function as such. kwargs is any additional args that need to be passed. Section class is the actual class. expected is a file name in the tests/expected directory with the expected text
def test_section_render(template:str,
                        template_folder:str,
                        kwargs:dict,
                        section_class:Section,
                        fixtures:list,
                        expected:str,
                        request):
        for fixture in fixtures:
             request.getfixturevalue(fixture)
        if template is not None:
             kwargs["template"] = template
        if template_folder is not None:
             kwargs["template_folder"] = template_folder

        sect = section_class(**kwargs)
        with open(os.path.join("expected",expected),"r") as f:
            print(sect.render())
            x = f.read()
            print(x)
            assert sect.render() == x
    

def test_individual_rss_feed_process(mock_feedparser_parse):
    rss = IndividualRSSFeed("http://test_individual_rss.com/feed")
    data = rss._process()
    with open(os.path.join("expected","individual_rss_process.json",)) as f:
        x = json.load(f)
    for item in x["items"]:
         item["pub_date"] = datetime.datetime.fromisoformat(item["pub_date"])
    assert x == data