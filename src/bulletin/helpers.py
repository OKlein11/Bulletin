import inspect
import os
import jinja2

def get_template(base_obj) -> jinja2.Template:
    if hasattr(base_obj,"template"):
        template = base_obj.template
        folder = base_obj.template_folder
    else:
        template = base_obj.__class__.default_template
        folder = os.path.join(os.path.dirname(inspect.getfile(base_obj.__class__)), "templates")


    template_loader = jinja2.FileSystemLoader(searchpath= folder)


    template_env = jinja2.Environment(loader=template_loader)
    return template_env.get_template(template)
