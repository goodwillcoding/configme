
"""
File Generator module.
"""

from abc import ABCMeta
from abc import abstractmethod

from io import open as io_open

from .exceptions import InvalidName


# --------------------------------------------------------------------------- #
class BaseTemplateRenderer(object):
    """
    **BaseTemplateRenderer an abstract class**

    Teamplate Renderers are responsible for rendering the templates and
    generating individual config file for a given role. It is meant to be used
    internally by :class:`Role`.

    The TemplateRenderer accepts the following arguments:

    :param path:

        The file path to the config template relative to the role's output
        path. This corresponds to the to the section name in the
        :term:`settings file`.

        The path should be have consist of characters considered valid for
        a file name on the operating system it is run on. It must also be a
        correct section name in the INI style settings file. Additionally it
        must be at least marginally human readable.

        As such due to difficulty maintaining OS specific forbidden characters
        set, complying with ini file specifications, and keeping readability
        a set of forbidden characters have choosen.

        The naming rules are:

         - name cannot start with a: `space` `/` `../` `./`
         - name cannot contain: `/../` `/./` `<` `>` `:` `"` `/` `|` `?` `*`

    :type path: str

    :param settings:

        A dictionary containing parsed and interpolated settings from the
        settings file for this section.

    :type settings: <dict>

    :raises:

        NameError is raised upon initialization if the name is does not match
        the naming requirements.
    """

    _FORBIDDEN_START_CHARS = (" ", "/", "../", "./")
    _FORBIDDEN_CHARS = ("/../", "/./", "<", ">", ":", '"', "/", "|", "?", "*")

    __metaclass__ = ABCMeta

    # ....................................................................... #
    config = None

    # ....................................................................... #
    role_output_folder_path = None

    # ....................................................................... #
    path = None

    # ....................................................................... #
    settings = None

    # ....................................................................... #
    def __init__(self, config, role_output_folder_path, path, settings):
        """
        See :class:`FileGenerator` class for initialization arguments
        documentation.
        """

        self.config = config
        self.role_output_folder_path = role_output_folder_path
        self.path = self.validate_path(path)

        self.settings = settings

    # ....................................................................... #
    @property
    def output_file_path(self):
        """
        :return:

            Path to the output config file. The path is computed by combining
            output role's output path with name of the template. Please
            remember the name of the template is also its full path.

            This is computed readonly property.

        :rtype: str
        """
        # TODO: switch to asset management
        asset_manager = self.config._asset_manager
        return asset_manager.join_path(
            (self.role_output_folder_path,
             asset_manager.path_filename(self.path)
            ))

    # ....................................................................... #
    def create_output_folder(self):
        """
        Create the output folder specified in `output_folder_path`.
        If the parents for the folder do not exist they will be created as
        well (same behaviour as mkdir -p).

        If there is not the config file path has no folder, then do not create
        any folder, but simply return the role folder

        :return: path to the the created output folder.
        :rype: str

        :raises:

            AssetLocationTaken - if there is already an asset or location
            at the output_folder path
        """

        asset_manager = self.config._asset_manager

        config_file_folder = asset_manager.path_dirname(self.path)

        # if there is no folder for this config file just return the role path
        if config_file_folder == '':
            return self.role_output_folder_path

        # other wise computer the entire folder and create it
        output_folder_path = asset_manager.join_path(
            (self.role_output_folder_path, config_file_folder))

        # check if the asset or location already exist at this path
        # fyi, this may araise AssetLocationTaken error
        asset_manager.asset_or_location_exists(output_folder_path)

        # create folder
        asset_manager.create_folder(output_folder_path)

        return output_folder_path

    # ....................................................................... #
    @abstractmethod
    def get_rendered_config(self):
        """
        **This is an abstract method that needs to be implemented by
        individual template renderers**

        Return and render template at path, interpolating the settings into it
        and return the stream with the template.

        :return: rendered template
        :rtype: str/unicode
        """

        pass

    # ....................................................................... #
    def write(self, _io_open=io_open):
        """
        Render and output config to file at `output_file_path`.

        :return: path to the the generated config file.
        :rype: str
        """

        self.create_output_folder()

        # TODO: exception handling
        file_handler = _io_open(self.output_file_path, 'w')
        file_handler.write(self.get_rendered_config())
        file_handler.close()

        return self.output_file_path

    # ....................................................................... #
    @classmethod
    def validate_path(cls, path):
        """
        Validate path. See class initialization documentation for naming
        requirements.

        :param name: path
        :type name: str/unicode

        :return: given path
        :rtype: str/unicode

        :raises: InvalidName, if path is invalid.
        """

        # starting if name begins with any starting characters
        for char in cls._FORBIDDEN_START_CHARS:
            if path.startswith(char):
                raise InvalidName("Path cannot start with '%s': %s"
                    % (char, path))

        # check is name contains any forbidden chars
        for char in cls._FORBIDDEN_CHARS:
            if char in path:
                raise InvalidName("Path cannot contain '%s': %s"
                    % (char, path))

        return path
