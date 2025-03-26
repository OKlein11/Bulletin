import pytest
import smtplib
import os
import feedparser
import json
import requests

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

@pytest.fixture(autouse=True)
def change_directory(monkeypatch):
    monkeypatch.chdir("tests")

@pytest.fixture
def mock_feedparser_parse(monkeypatch:pytest.MonkeyPatch):

    def mock_feed_get(link:str, *args):

        name:str = link.split("//")[1].split(".")[0]
        with open(os.path.join("data",f"{name}.txt")) as f:
            return bytes(f.read(), encoding="utf-8")
        


    monkeypatch.setattr(feedparser.http,"get",mock_feed_get)

def mock_process_function(config):
    return {"test":"test"}


class mock_request:
    def __init__(self,url,headers):
        self.name = url.split("//")[1].split(".")[0]

    def json(self) -> dict:
        with open(os.path.join("data",f"{self.name}.json")) as f:
            return json.load(f)
    
    def content(self) -> str:
        with open(os.path.join("data",f"{self.name}.txt")) as f:
            return f.read()
    @property
    def status_code(self):
        return 200
        
@pytest.fixture
def mock_request_get(monkeypatch):
    def mock_get(url,headers):
        return mock_request(url,headers)
    
    monkeypatch.setattr(requests,"get",mock_get)