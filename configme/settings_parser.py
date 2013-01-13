# -*- coding: utf-8 -*-

"""
Module is responsible for parsing settings files and providing access to
settings.
"""

from ConfigParser import Error as ConfigParserError
from ConfigParser import SafeConfigParser

from .exceptions import SettingsParsingError


# --------------------------------------------------------------------------- #
class SettingsParser(object):
    """
    This class is responsible for reading the settings from a given location
    and providing access to its content.

    :param file_path: path the settings file
    :type file_path: str/unicode

    :param variables: optional, variables to interpolate into settings file.
    :type variables: dict
    """

    file_path = None
    _parser = None

    # ....................................................................... #
    def __init__(
        self,
        file_path,
        variables=None,
        _config_parser_factory=SafeConfigParser):

        # handle mutable default for variables paramater
        if variables is None:
            variables = {}

        self.file_path = file_path
        self._parser = _config_parser_factory(defaults=variables)

    # ....................................................................... #
    def read(self):
        """
        Read and parse settings file for the given file path.

        Return a list of tuples where the tuplle first element is
        config file name and the second element is dictionary
        of settings for that config file name.

        (Section named "DEFAULT" is not included in the list)

        :raises:
            SettingsParsingError if file could not be found, read, parsed
            or if variables could not be interpolated.
        """

        result = []

        try:
            loaded_files = self._parser.read(self.file_path)
        except ConfigParserError as err:
            raise SettingsParsingError(
                'Could not parse file: %s.\n\nMore Info:\n%s'
                % (self.file_path, err.message))

        if not self.file_path in loaded_files:
            raise SettingsParsingError('Could not load file: %s'
                % self.file_path)

        try:
            # ConfigParserError may be thrown on .items() call
            result = [(section_name, dict(self._parser.items(section_name)))
                for section_name in self._parser.sections()]
        except ConfigParserError as err:
            raise SettingsParsingError(
                "Bad variable interpolation for file: %s\n\n%s"
                % (self.file_path, err.message))

        return result
