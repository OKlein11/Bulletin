import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Sequence

class EmailServer:
    def __init__(self,auth_user:str,auth_password:str,server:str,port:int=587) -> None:
        self.server:smtplib.SMTP = smtplib.SMTP(server,port)
        self.sender:str = auth_user
        self.server.starttls()
        self.server.login(auth_user,auth_password)

    def __del__(self):
        self.server.quit()

    def send(self,send_to: str | Sequence[str],subject:str,text:str) -> None:
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = send_to
        text = MIMEText(text,"html")
        msg.attach(text)
        self.server.sendmail(self.sender,send_to,msg.as_string())
