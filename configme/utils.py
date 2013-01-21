# -*- coding: utf-8 -*-

"""
Miscellaneous Utilities
"""

from logging import Filter


# --------------------------------------------------------------------------- #
class AllowedLevelsFilter(Filter):
    """
    LevelFilter is subclass of :class:`logging.Filter` responsible for
    filtering out any levels except the ones specified at class initialization.

    :param levels: list of logging levels to allow.
    :type: tuple/list or any other iterable

    Example code ::

        >>> import logging
        >>> logger_ = logging.getLogger('test_logger')
        >>> level_filter = LevelFilter([logging.INFO, logging.CRITICAL])
        >>> logger_.addFilter(level_filter)

        >>> logger_.info("hello")
        >>> logger_.warn("happy")
        >>> logger_.critical("puppy")

    Produces following output ::

        hello
        puppy
    """
    # ....................................................................... #
    def __init__(self, levels):
        """
        See module description
        """
        self._levels = levels

    # ....................................................................... #
    def filter(self, record):
        """
        Filter logging records.

        :return: True if logging record is of an allowed logging level,
                 otherwise False
        :rtype: bool
        """
        return record.levelno in self._levels
