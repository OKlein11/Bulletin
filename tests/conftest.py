import pytest
import smtplib

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
def test_process_function(config):
    return {"test":"example"}
