import jinja2
import inspect
import os
from typing import Callable

class Section:
    def __init__(self,process_function:Callable,template:str,config={}):
        self.config = config
        self.process_function = process_function
        self.template = template


    def _process(self, func:Callable = None):
        if func is None:
            return self.process_function(self.config)
        else:
            return func(self.config)


    def render(self):
        data = self._process()
        template_loader = jinja2.FileSystemLoader(searchpath= os.path.join(os.path.dirname(inspect.getfile(self.__class__)), "templates"))
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(self.template)

        return template.render(data=data)