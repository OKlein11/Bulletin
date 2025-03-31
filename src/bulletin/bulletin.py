from .section import Section
from .email_server import EmailServer
from typing import Sequence
from .helpers import get_template

DEFAULT_TEMPLATE_FOLDER = "templates"

class Bulletin:
    """
    The base class to define bulletins

    Attributes
    -----
    default_template : str
        The default template of the bulletin. Defined at a class level

        default is base.html

    email_server : EmailServer
        The email server the bulletin should use to send emails

    config : dict, optional
        The configuration for the Bulletin
    sections: list[Section]
        The sections used in this Bulletin
    template_folder : str
        The template folder where a non-default template is stored
    template : str
        The name of a non-default template file
    """
    default_template: str = "base.html"
    def __init__(self,
                 email_server:EmailServer,
                 config:dict={"subject":"Bulletin"},
                 template:str = None, 
                 template_folder = DEFAULT_TEMPLATE_FOLDER
                 ) -> None:
        """
        Parameters
        -----
        email_server : EmailServer
            The email server for the object to use
        config: dict,optional
            The configuration of the object
        template : str, optional
            The name of a template file within the template_folder directory. Will be used in place of the class' default template
        template_folder : str, optional
            The path relative to the current working directory where a non-default template is stored.
        """
        self.email_server: EmailServer = email_server
        self.config:dict = config
        self.sections: list[Section] = []
        self.template_folder = template_folder
        if template is not None:
            self.template = template

    def add_section(self,section: Section) -> list[Section]:
        """
        Adds a section to the bulletin

        Parameters
        -----
        section : Section
            The section to be added to this bulletin
        Returns
        -----
        list[Section]
            returns the object's sections attribute after adding a new section
        """
        if isinstance(section,Section):
            self.sections.append(section)
        return self.sections


    def render(self) -> str:
        """
        Renders the bulletin

        Returns
        -----
        str
            returns the rendered template for the bulletin
        """
        renders = [section.render() for section in self.sections]
        template = get_template(self)
        return template.render(content = renders)


    def send(self,recepient: str | Sequence[str],subject: str | None = None) -> None:
        """
        Sends the bulletin via email

        Parameters
        -----
        recepient : str | Sequence[str]
            The address or addresses to send the email too
        subject: str, optional
            Changes the subject of the email to something other than the default defined on object creation
        """
        text = self.render()
        subj = self.config["subject"]
        if subject is not None:
            subj = subject
        self.email_server.send(recepient,subj,text)

