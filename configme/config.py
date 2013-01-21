# -*- coding: utf-8 -*-

"""
Config Generator
"""

from .assets import AssetManager
from .settings import SettingsParser
from .renderers.jinja2_rendering import Jinja2TemplateRenderer


# --------------------------------------------------------------------------- #
class Configurator(object):
    """
    Configurator is class responsible for setting up and maining configuration
    settings for any given role. It is also responsible for access
    settings parser and template renderer.


    :param templates_path:

        Path to the top level folder containing the config templates. The
        config files are specified as the sections name are appended to this
        path.

        :raises: :class:`LocationNotFound` if the directory does not exist.

        Let's say the top template path is '/tmp/foo' and we have a nginx
        config generated etc/nginx/nginx.conf. This will correspond to the
        following:

        Code:
            Config(templates_path = '/tmp/foo', ...)

        Role file:
            [etc/nginx/nginx.conf]

    :type templates_path: str/unicode


    :param settings_path:

        Path to the folder containing .settings files for roles.

        :raises: :class:`LocationNotFound` if the folder does not exist.

    :type settings_path: str/unicode


    :param output_path:

        Path to the folder where the role folders and configs are written to.

        :raises: :class:`LocationNotFound` if the folder does not exist.

    :type output_path: str/unicode


    :param settings_file_extension:

        File extension for the role files. Defaults to 'settings'. Has to
        conform to the operating system's file name standards.

        For example a role of "alpha" woth the default settings_file_extension
        of 'settings' would requires an 'alpha.settings' file in the
        `settings_path` folder.


    :raises:

        :class:`LocationNotFound` if any of the arguments that take folders
        paths are set to folders that do not exist.
    """

    _templates_path = None
    _settings_path = None
    _output_path = None
    _settings_parser_factory = None
    _template_renderer_factory = None
    _asset_manager_factory = None

    _asset_manager = None

    # ....................................................................... #
    @property
    def templates_path(self):
        return self._templates_path

    # the noqa below is to disable pyflake check W806, redefinition of function
    @templates_path.setter  # NOQA
    def templates_path(self, value):
        self._templates_path = self._asset_manager.location(value, "template")

    # ....................................................................... #
    @property
    def settings_path(self):
        return self._settings_path

    # the noqa below is to disable pyflake check W806, redefinition of function
    @settings_path.setter  # NOQA
    def settings_path(self, value):
        self._settings_path = self._asset_manager.location(value, "settings")

    # ....................................................................... #
    @property
    def output_path(self):
        return self._output_path

    # the noqa below is to disable pyflake check W806, redefinition of function
    @output_path.setter  # NOQA
    def output_path(self, value):
        self._output_path = self._asset_manager.location(value, "output")

    # ....................................................................... #
    settings_file_extension = None

    # ....................................................................... #
    def __init__(self,
                 templates_path,
                 settings_path,
                 output_path,
                 settings_file_extension='settings',
                 _settings_parser_factory=SettingsParser,
                 _template_renderer_factory=Jinja2TemplateRenderer,
                 _asset_manager_factory=AssetManager):

        # set factories
        self._settings_parser_factory = _settings_parser_factory
        self._template_renderer_factory = _template_renderer_factory
        self._asset_manager_factory = _asset_manager_factory

        # create asset manager since we will need it for property setting
        self._asset_manager = self._asset_manager_factory()

        # now set the properties
        self.templates_path = templates_path
        self.settings_path = settings_path
        self.output_path = output_path
        self.settings_file_extension = settings_file_extension
