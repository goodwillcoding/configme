# -*- coding: utf-8 -*-

"""
Argument Parser
"""

from argparse import Action
from argparse import ArgumentParser

from .exceptions import ScriptArgumentError


# --------------------------------------------------------------------------- #
class CliArgumentParser(ArgumentParser):
    """
    Variant of ArgumentParser that does not exit on error but instead throws
    an :class:`ScriptArgumentsError` exception on error.

    This class overwrites so called `Exiting methods
    <http://docs.python.org/library/argparse.html#exiting-methods>`_ of
    ArgumentParser.
    """

    # ....................................................................... #
    def __init__(self, *args, **kwargs):
        ArgumentParser.__init__(self, *args, **kwargs)

    # ....................................................................... #
    def error(self, message):
        """
        :raise: :class: `ScriptArgumentsError` for any error message.
        """
        raise ScriptArgumentError(message)

    # ....................................................................... #
    def exit(self, *args, **kwargs):  # pragma: no cover
        """
        Disabled the exit method, so we never exit.
        """
        pass

    # ....................................................................... #
    def parse(
        self,
        args,
        _parse_args_method=ArgumentParser.parse_args  # for testing
    ):
        """

        Calls :class:`ArgumentParser.parse_args` with given args. raises
        ScriptArgumentsError if numbers arguments given is 0. The error
        message contains formatted help.

        :param args: sysv style arguments, without the script name
        :type args: list/tuple

        :raises:

            :class: `ScriptArgumentsError` for with any argparse error message
            or no script arguments were provided.
        """

        # default to printing help if no arguments were specified
        if len(args) == 0:
            raise ScriptArgumentError(
                "No script arguments specified\n\n%s" % self.format_help())

        return _parse_args_method(self, args)

    # ....................................................................... #
    class ArgListToDictAction(Action):
        """
        Action for argparse that converts list of 2 member tuples into a
        dictionary.
        """

        # ................................................................... #
        def __init__(self, option_strings, dest, *args, **kwargs):
            Action.__init__(self, option_strings, dest, *args, **kwargs)

        # ................................................................... #
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, dict(values))

    # ----------------------------------------------------------------------- #
    @staticmethod
    def split_argument(string):
        """
        Split the given string ":" or "=" separated strings to a two element
        tuple. If both ":" and "=" are present in the string the first one
        is used as a separator.

        :param args_list:

            string separated by either ":" or "=" (which ever comes first).

        :return: two element tuple split by : or = where first element args
                 key and second element as value.
        :rtype: tuple

        :raises: ScriptArgumentError if neither ":" nor "=" separator are not
                 present in the given string.
        """

        # find the separator
        colon_pos = string.find(":")
        equal_pos = string.find("=")

        if (colon_pos == -1) and (equal_pos == -1):
            raise ScriptArgumentError(
                "List element '%s' is missing a separator, either ':' or '='"
                % string)

        # remove the -1 if it exists and grab the closest position
        separator_pos = min(val for val in [colon_pos, equal_pos] if val != -1)
        # return (key, value)
        return (string[:separator_pos], string[separator_pos + 1:])
