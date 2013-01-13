# -*- coding: utf-8 -*-

"""
CLI logging
"""

import logging
from logging import StreamHandler


# --------------------------------------------------------------------------- #
def cli_logger_factory(name, out, err):
    """
    Setup basic logging and return logger instance

    :return:

        logger instance with following setup:

            - DEBUG and INFO will be printed to `out`.
            - WARN/WARNING, ERROR, and CRITICAL will be printed to `err`.

    :rtype: logging.Logger
    """

    logger_ = logging.getLogger(name)
    logger_.setLevel(logging.DEBUG)

    # handles DEBUG and INFO
    handler_out = StreamHandler(out)
    level_filter = AllowedLevelsFilter([logging.DEBUG, logging.INFO])
    handler_out.addFilter(level_filter)
    logger_.addHandler(handler_out)

    # handles WARNING, ERROR, and CRITICAL
    handler_err = StreamHandler(err)
    level_filter = AllowedLevelsFilter(
        [logging.WARNING, logging.ERROR, logging.CRITICAL])

    handler_err.addFilter(level_filter)
    logger_.addHandler(handler_err)

    return logger_


# --------------------------------------------------------------------------- #
class AllowedLevelsFilter(logging.Filter):
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
