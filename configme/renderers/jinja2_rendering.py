# -*- coding: utf-8 -*-

"""
Jinja2 Template Renderer.
"""

from ..rendering import BaseTemplateRenderer

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import TemplateError

from ..exceptions import TemplateRenderError


# --------------------------------------------------------------------------- #
class Jinja2TemplateRenderer(BaseTemplateRenderer):
    """
    Jinja2 Template Renderer.
    """

    jinja2_env = None

    # ....................................................................... #
    def __init__(
        self,
        config,
        role_output_folder_path,
        path,
        settings,
        _jinja2_filesystem_loader_factory=FileSystemLoader,
        _jinja2_environment_factory=Environment
    ):

        BaseTemplateRenderer.__init__(
            self, config, role_output_folder_path, path, settings)

        # setup jinja2 file system template loading
        loader = _jinja2_filesystem_loader_factory(
            searchpath=self.config.templates_path)
        self.jinja2_env = _jinja2_environment_factory(loader=loader)

    # ....................................................................... #
    def get_rendered_config(self):
        """
        Render and output config to file at `output_file_path`.

        :return: path to the the generated config file.
        :rype: str

        :raises:

            :class:`TemplateRenderError` for any template look up or render
            error.
        """

        # retrieve the template and render it
        try:
            template = self.jinja2_env.get_template(self.path)
            output = template.render(**self.settings)
        except TemplateError as err:
            msg = 'Failed to render config template: %s\n\n%s' \
                % (self.path, err.message)
            raise TemplateRenderError(msg)

        return output
