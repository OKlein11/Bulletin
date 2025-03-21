import pytest
import smtplib
import os
import feedparser


class MockSmtp:

    def __init__(self,server,port):
        self.server = server
        self.port = port

    @staticmethod
    def starttls():
        pass

    def login(self,username,password):
        self.username = username
        self.password = password


    def sendmail(self,sender,recepient,msg):
        self.msg = msg
        self.sender = sender
        self.recepient = recepient

    def quit(self):
        pass
        

@pytest.fixture
def mock_get_smtp_server(monkeypatch):

    def mock_smtp(*args,**kwargs):
        return MockSmtp(*args,**kwargs)
    
    monkeypatch.setattr(smtplib,"SMTP",mock_smtp)


@pytest.fixture
def mock_feedparser_parse(monkeypatch:pytest.MonkeyPatch):

    def mock_feed_get(link:str, *args):

        name:str = link.split("//")[1].split(".")[0]
        with open(os.path.join("data",f"{name}.txt")) as f:
            return bytes(f.read(), encoding="utf-8")
        

    monkeypatch.chdir("tests")
    monkeypatch.setattr(feedparser.http,"get",mock_feed_get)

def mock_process_function(config):
    return {"test":"test"}