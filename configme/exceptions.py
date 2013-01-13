# -*- coding: utf-8 -*-

"""
This modules contains ConfugMe exception classes. Each  class is a subclass of
:class:`ConfigMeException`.
"""


# --------------------------------------------------------------------------- #
class ConfigMeException(Exception):
    """
    Base class for all ConfigMe Exceptions`.
    """
    pass


# --------------------------------------------------------------------------- #
class ScriptArgumentError(ConfigMeException):
    pass


# --------------------------------------------------------------------------- #
class LocationNotFound(ConfigMeException):
    pass


# --------------------------------------------------------------------------- #
class InvalidName(ConfigMeException):
    pass


# --------------------------------------------------------------------------- #
class LocationRemovalError(ConfigMeException):
    pass


# --------------------------------------------------------------------------- #
class LocationCreationError(ConfigMeException):
    pass


# --------------------------------------------------------------------------- #
class AssetLocationTaken(ConfigMeException):
    pass


# --------------------------------------------------------------------------- #
class SettingsParsingError(ConfigMeException):
    pass
