import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Sequence

class EmailServer:
    """
    A class used to create an smtp server connection, then send emails over it.

    ...

    Attributes
    --------
    server : smtplib.SMTP
        The smtp server connection
    sender : str
        The email used to authenticate with the server. Also used as the sender when sending emails

    Methods
    -------
    send(send_to: str | Sequence[str], subject: str, text: str)
        Sends an email to the addresses given, with the given subject and text lines
    
    """
    def __init__(self,auth_user:str,auth_password:str,server:str,port:int=587) -> None:
        """
        Parameters
        --------
        auth_user : str
            The username for logins. Will also be used as the sender when sending emails
        auth_password : str
            The password for logins.
        server : str
            The smtp server url
        port : int, optional
            The port on which to connect to the smtp server. Default value 587
        """
        self.server:smtplib.SMTP = smtplib.SMTP(server,port)
        self.sender:str = auth_user
        self.server.starttls()
        self.server.login(auth_user,auth_password)

    def __del__(self):
        self.server.quit()

    def send(self,send_to: str | Sequence[str],subject:str,text:str) -> None:
        """
        This method sends an email using the authenticated server saved within the object

        Parameters
        ---------
        send_to : str | Sequence[str]
            The address or addresses to send the emails to
        subject : str
            The subject line of the email
        text : str
            The text of the email
        """
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = send_to
        text = MIMEText(text,"html")
        msg.attach(text)
        self.server.sendmail(self.sender,send_to,msg.as_string())
