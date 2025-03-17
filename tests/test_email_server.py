from bulletin.email_server import EmailServer
import pytest
import smtplib


    

def test_email_server_init(mock_get_smtp_server):
    server = EmailServer("test@example.com","password1","example.example.com")
    assert server.sender == "test@example.com"

def test_email_server_send(mock_get_smtp_server):
    sender = "test@example.com"
    recepient = "testing@testing.com"
    subject = "This is a test"
    msg = "This is a message"
    server = EmailServer(sender,"password1","example.example.com")
    server.send(recepient,subject,msg)
    assert server.server.sender == sender
    assert server.server.recepient == recepient
    assert msg in server.server.msg