from bulletin.helpers import *
from bulletin.section import Section
from bulletin.bulletin import Bulletin
from bulletin.email_server import EmailServer
import pytest
from conftest import mock_process_function
import os

@pytest.mark.parametrize(("template","template_folder","kwargs","expected"),
                         [
                             (None,None,{},"get_template_helper_section_default.txt"),
                             ("section.html",None,{},"get_template_helper_section_template.txt"),
                             ("section.html","templates_2",{},"get_template_helper_section_template_folder.txt"),
                         ])
def test_get_template_helper_section(template,template_folder,kwargs,expected,monkeypatch):
    for k,v in {"template":template,"template_folder":template_folder}.items():
        if v is not None:
            kwargs[k] = v
    with open(os.path.join("expected",expected)) as f:
        expect = f.read()
    sect = Section(mock_process_function,**kwargs)
    data = sect._process()
    template = get_template(sect)
    assert template.render(data=data) == expect


@pytest.mark.parametrize(("template","template_folder","kwargs","expected"),
                         [
                             (None,None,{},"get_template_helper_bulletin_default.txt"),
                             ("base.html",None,{},"get_template_helper_bulletin_template.txt"),
                             ("base.html","templates_2",{},"get_template_helper_bulletin_template_folder.txt"),
                         ])
def test_get_template_helper_bulletin(template,template_folder,kwargs,expected,monkeypatch,mock_get_smtp_server):
    for k,v in {"template":template,"template_folder":template_folder}.items():
        if v is not None:
            kwargs[k] = v
    with open(os.path.join("expected",expected)) as f:
        expect = f.read()
    sect = Section(mock_process_function)
    server = EmailServer("test","test","test.example.com")
    bullet = Bulletin(server,**kwargs)
    bullet.add_section(sect)
    renders = [section.render() for section in bullet.sections]
    template = get_template(bullet)
    assert template.render(content=renders) == expect