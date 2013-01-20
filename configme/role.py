# -*- coding: utf-8 -*-

"""
Role Generator module.
"""

from .exceptions import InvalidName


# --------------------------------------------------------------------------- #
class Role(object):
    """
    Role is responsible for generating all the configs files for a
    given role.

    The Role accepts the following arguments:

    :param config:

        Configuration for the app

    :type config: :class:`configme.Config`

    :param name:

        The name of the role. Combination of the role name + settings extension
        that is set in  the config corresponds the :term:`settings file` in the
        settings path.

        The name should be have consist of characters considered valid for
        a file name on the operating system it is run on. It must also be a
        correct section name in the INI style settings file. Additionally it
        must be at least marginally human readable.

        As such due to difficulty maintaining OS specific forbidden characters
        set, complying with INI file specifications, and keeping readability
        a set of forbidden characters have chosen.

        The naming rules are:

         - name cannot start with a: `space`
         - name cannot contain: `<` `>` `:` `'` `"` `/` `\\` `|` `?` `*` `\``

        Examples of roles are: production, stage, development, alpha

    :type name: str/unicode

    :param suffix:

        Optional, role suffix is used to generate of the role's folder name.
        When specified, the folder name containing the generated configs will
        be <role name><suffix>. See `suffixed_name` computed property for more
        information. Defaults to an empty string.

        The suffix must conform to the same naming standards as the name
        `property`.

    :type suffix: str/unicode

    :param variables:

        Optional, a dictionary containing variables for in interpolation of
        roles settings.

    :type variables: <dict>

    :raises:

        :class:`InvalidName` is raised upon initialization if the name is does
        not match the naming requirements.

    """

    _FORBIDDEN_START_CHARS = (" ",)
    _FORBIDDEN_CHARS = ("<", ">", ":", '"', "'", "/", "\\", "|", "?", "*", "`")

    _name = None

    # suffix defaults is an empty string
    _suffix = ''

    # ....................................................................... #
    config = None

    # ....................................................................... #
    @property
    def name(self):
        return self._name

    # the noqa below is to disable pyflake check W806, redefinition of function
    @name.setter  # NOQA
    def name(self, value):
        self._name = self.validate_role_name(value)

    # ....................................................................... #
    @property
    def suffix(self):
        return self._suffix

    # the noqa below is to disable pyflake check W806, redefinition of function
    @suffix.setter  # NOQA
    def suffix(self, value):
        self._suffix = self.validate_role_name(value)

    # ....................................................................... #
    variables = None

    # ....................................................................... #
    @property
    def suffixed_name(self):
        """
        :return:

            Suffixed role name used for role folder name creation.
            If suffix is specified during initialization then the folder's name
            will be: <role name><suffix>.

            This is computed readonly property.

        :rtype: str/unicode
        """

        # add suffix to the role name.
        # fyi, the suffix default is an empty string so it covers that case
        # as well
        return "%s%s" % (self.name, self.suffix)

    # ....................................................................... #
    @property
    def output_folder_path(self):
        """
        :return:

            Path to the output role folder. The path is computed by
            combining role's output path with the `suffixed_name`.

            This is computed readonly property.

        :rtype: str/unicode
        """
        path_join = self.config._asset_manager.path_join
        return path_join((self.config.output_path, self.suffixed_name))

    # ....................................................................... #
    @property
    def settings_file_path(self):
        """
        :return:

            Path for role's :term:`settings file` file computed like so:
            <config.settings_path> +
            <role name>.<config.settings_file_extension>

        :rtype: str/unicode
        """
        path_join = self.config._asset_manager.path_join
        file_name = "%s.%s" % (self.name, self.config.settings_file_extension)
        return path_join((self.config.settings_path, file_name))

    # ....................................................................... #
    def __init__(self, config, name, suffix='', variables=None):

        self.name = name
        self.suffix = suffix
        self.config = config

        # handle mutable defaults
        if variables is None:
            variables = {}

        self.variables = variables

    # ....................................................................... #
    def write_configs(self):
        """
        Create role folder. Then go over each config file creating parent
        folders. Interpolate settings into a config file and write it
        out to a file

        :return: sorted list of all the folders and files created.
        :rtype: list

        :raises:

            :class:`LocationRemovalError` if old role folder could not be
            removed. This exception bubbled up from AssetsManager.

            :class:`LocationCreationError` if role folder could not be created.
            This exception bubbled up from AssetsManager.

            :class:`SettingsParsingError`: if could not load parse the given
            config file or variables for any section could not be interpolated.
            This exception bubbled up from SettingsParser.
        """

        # list used to record folders and files created
        output_list = []

        # create the top level folder which will contain all the configs
        # this may raise LocationRemovalError or LocationCreationError
        asset_manager = self.config._asset_manager
        asset_manager.remove_folder(self.output_folder_path)
        asset_manager.create_folder(self.output_folder_path)

        # load and parse the settings files and return the the template
        # renderer instances generator.
        # fyi, this may raise SettingsParsingError
        settings_parser = self.config._settings_parser_factory(
            file_path=self.settings_file_path,
            variables=self.variables)

        # iterate over file generators, creating their parent folders and
        # then rendering templates to file
        # record folder and file creation
        # fyi, .read() may raise SettingsParsingError exception
        for relative_file_path, settings in settings_parser.read():
            # create renderer
            template_renderer = self.config._template_renderer_factory(
                self.config,
                self.output_folder_path,
                relative_file_path,
                settings)

            # create renderer parent folder (recursively)
            output_file_path = template_renderer.write()
            # record the rendered config location
            output_list.append(output_file_path)

        # sort the output list
        output_list.sort()

        return output_list

    # ....................................................................... #
    @classmethod
    def validate_role_name(cls, name):
        """
        Validate role name. See class initialization documentation for naming
        requirements.

        :param name: role name
        :type name: str/unicode

        :return: given name
        :rtype: str/unicode

        :raises: InvalidName, if role name is invalid.
        """

        # starting if name begins with any starting characters
        for char in cls._FORBIDDEN_START_CHARS:
            if name.startswith(char):
                raise InvalidName("Role name cannot start with '%s': %s"
                    % (char, name))

        # check is name contains any forbidden chars
        for char in cls._FORBIDDEN_CHARS:
            if char in name:
                raise InvalidName("Role name cannot contain '%s': %s"
                    % (char, name))

        return name
