from bulletin.section import *
import pytest
import json

def mock_process_function(config):
    return {"test":"test"}


def test_section_init():
    section = Section(mock_process_function)
    assert section.config == {}
    assert not(hasattr(section,"template"))
    assert section.template_folder == "templates"
    assert section.default_template == "section.html"


@pytest.mark.parametrize(("section_class","kwargs","expected"),[
(Section,{"process_function":mock_process_function},{"config":{},"template_folder":"templates","default_template":"section.html"})
])
def test_section_init_p(section_class:Section,kwargs:dict,expected:dict):
    section = section_class(**kwargs)
    for k,v in expected.items():
        assert getattr(section,k) == v
    if "template" not in kwargs.keys():
        assert not(hasattr(section,"template"))


@pytest.mark.parametrize(("kwargs","section_class","expected",),[
     ({"process_function":mock_process_function},Section,"section_process.json")
])
def test_section_process(kwargs:dict,
                         section_class:Section,
                         expected:str):
     section = section_class(**kwargs)
     with open(os.path.join("tests","expected",expected)) as f:
          assert json.load(f) == section._process()


@pytest.mark.parametrize(("template","template_folder","kwargs","section_class","expected"),[
                          (None,None,{"process_function":mock_process_function},Section,"section_render_default.txt"),
                          ("section.html",None,{"process_function":mock_process_function},Section,"section_render_template.txt"),
                          ("section.html","templates_2",{"process_function":mock_process_function},Section,"section_render_template_folder.txt"),
                          (None,"templates_2",{"process_function":mock_process_function},Section,"section_render_default.txt"),
                         ])
# Tests the render function. Should be anonymized to work with any Section subclass
# template and template folder are passed to the Section.__init__ function as such. kwargs is any additional args that need to be passed. Section class is the actual class. expected is a file name in the tests/expected directory with the expected text
def test_section_render(template:str,
                        template_folder:str,
                        kwargs:dict,
                        section_class:Section,
                        expected:str,
                        monkeypatch:pytest.MonkeyPatch):
        if template is not None:
             kwargs["template"] = template
        if template_folder is not None:
             kwargs["template_folder"] = template_folder
        monkeypatch.chdir(os.path.join(os.path.curdir,"tests"))

        sect = section_class(**kwargs)
        with open(os.path.join("expected",expected),"r") as f:
                assert sect.render() == f.read()
    
    