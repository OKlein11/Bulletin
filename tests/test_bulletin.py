from bulletin.bulletin import Bulletin
from bulletin.email_server import EmailServer
from bulletin.section import Section
import pytest
from conftest import mock_process_function
import os

@pytest.mark.parametrize(("config","template","template_folder","expected"),
                         [
                             (None,None,None, {"config":{"subject":"Bulletin"},"template_folder":"templates","default_template":"base.html"})
                         ])
def test_bulletin_init(config,template,template_folder,expected,mock_get_smtp_server):
    server = EmailServer("test","test","test.example.com")
    kwargs = {"email_server":server}
    for key,value in {"config":config,"template":template,"template_folder":template_folder}.items():
        if value is not None:
            kwargs[key] = value
    bullet = Bulletin(**kwargs)
    for k,v in expected.items():
        assert getattr(bullet,k) == v
    if "template" not in kwargs.keys():
        assert not(hasattr(bullet,"template"))


def test_bulletin_add_section(mock_get_smtp_server):
    server = EmailServer("test","test","test.example.com")
    bullet = Bulletin(server)
    section = Section(mock_process_function)
    add_sec = bullet.add_section(section)
    assert add_sec == [section]
    assert bullet.sections == [section]


@pytest.mark.parametrize(("config","template","template_folder","expected"),
                         [
                             (None,None,None,"bulletin_render_default.txt")
                         ])
def test_bulletin_render(config,template,template_folder,expected,monkeypatch,mock_get_smtp_server):
    server = EmailServer("test","test","test.example.com")
    kwargs = {"email_server":server}
    for key,value in {"config":config,"template":template,"template_folder":template_folder}.items():
        if value is not None:
            kwargs[key] = value
    bullet = Bulletin(**kwargs)
    section = Section(mock_process_function)
    bullet.add_section(section)
    rendered = bullet.render()

    with open(os.path.join("expected",expected)) as f:
        expected_text = f.read()
    assert rendered == expected_text