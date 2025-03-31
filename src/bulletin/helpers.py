import inspect
import os
import jinja2

def get_template(base_obj: object) -> jinja2.Template:
    """
    This function contains the logic to get the correct Jinja template for rendering. The precedence is as following
        1. A file found at template_folder/template. Both template_folder and template need to be defined
        2. A file found at default_template_folder/template. template need to be defined
        3. A file found at bulletin_source_folder/templates/default_template.

    Parameters
    -----
    base_obj : object
        The object to find the template for. 

        This object should have attributes template folder and optionally template
    Returns
    -----
    jinja2.Template
        Returns the template to be rendered with
    """

    if hasattr(base_obj,"template"):
        template = base_obj.template
        folder = base_obj.template_folder
    else:
        template = base_obj.__class__.default_template
        folder = os.path.join(os.path.dirname(inspect.getfile(base_obj.__class__)), "templates")


    template_loader = jinja2.FileSystemLoader(searchpath= folder)


    template_env = jinja2.Environment(loader=template_loader)
    return template_env.get_template(template)
