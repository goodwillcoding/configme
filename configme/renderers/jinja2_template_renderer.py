# -*- coding: utf-8 -*-

"""
Jinja2 Template Renderer.
"""

from ..template_renderer import BaseTemplateRenderer

from jinja2 import Environment
from jinja2 import FileSystemLoader


# --------------------------------------------------------------------------- #
class Jinja2TemplateRenderer(BaseTemplateRenderer):
    """
    Jinja2 Template Renderer.
    """

    # ....................................................................... #
    def __init__(self, *args, **kwargs):
        BaseTemplateRenderer.__init__(self, *args, **kwargs)

        # jinja2 specific
        loader = FileSystemLoader(self.config.templates_path)
        self._jinj2_env = Environment(loader=loader)

    # ....................................................................... #
    def get_rendered_config(self):
        """
        Render and output config to file at `output_file_path`.

        :return: path to the the generated config file.
        :rype: str
        """

        # retrieve the template
        template = self._jinj2_env.get_template(self.path)
        # render and return
        return template.render(**self.settings)
