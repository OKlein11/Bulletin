from .section import Section
from .email_server import EmailServer
from typing import Sequence
import jinja2
import os
import inspect

DEFAULT_TEMPLATE_FOLDER = "templates"

class Bulletin:
    default_template = "base.html"
    def __init__(self,email_server:EmailServer,
                 config:dict={"subject":"Bulletin"},
                 template:str = None, 
                 template_folder = DEFAULT_TEMPLATE_FOLDER
                 ) -> None:
        self.email_server: EmailServer = email_server
        self.config:dict = config
        self.sections: list[Section] = []
        self.template_folder = template_folder
        if template is not None:
            self.template = template

    def add_section(self,section: Section) -> list[Section]:
        if isinstance(section,Section):
            self.sections.append(section)
        return self.sections


    def render(self):
        renders = [section.render() for section in self.sections]
        if hasattr(self,"template"):
            template = self.template
            folder = self.template_folder
        else:
            template = self.__class__.default_template
            folder = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), "templates")


        template_loader = jinja2.FileSystemLoader(searchpath= folder)


        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template)
        return template.render(content = renders)


    def send(self,recepient: str | Sequence[str],subject: str | None = None):
        text = self.render()
        subj = self.config["subject"]
        if subject is not None:
            subj = subject
        self.email_server.send(recepient,subj,text)

