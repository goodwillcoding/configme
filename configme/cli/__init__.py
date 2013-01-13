# -*- coding: utf-8 -*-
# package

import sys

from .cli_runner import CliRunner
from .cli_parser import CliArgumentParser

from ..version import PACKAGE_NAME
from ..version import PACKAGE_VERSION_FULL
from ..version import PACKAGE_LOGGER_NAME


# --------------------------------------------------------------------------- #
def configured_argument_parser(_argument_parser_factory=CliArgumentParser):

    """
    Setup and return a parser object with with configured command-line
    arguments.

    :return:

        argparse.ArgumentParser with configured command-line arguments.

    :rtype: argparse.ArgumentParser
    """

    parser = _argument_parser_factory(
        description='%s %s command line utility.'
        % (PACKAGE_NAME, PACKAGE_VERSION_FULL))

    # template path
    parser.add_argument(
        "-t",
        "--templates-path",
        required=True,
        help="Path to configuration templates folder."
        )

    # settings path
    parser.add_argument(
        "-s",
        "--settings-path",
        required=True,
        help="Path to settings folder."
        )

    # output path
    parser.add_argument(
        "-o",
        "--output-path",
        required=True,
        help="Path to output folder."
        )

    # role name
    parser.add_argument(
        "-r",
        "--role-name",
        required=True,
        help="Role name."
        )

    # role suffix
    parser.add_argument(
        "-u",
        "--role-suffix",
        required=False,
        default='',
        help="Role suffix."
        )

    # role vars, grab them and convert them to a dictionary
    parser.add_argument(
        "-b",
        "--role-variables",
        action=parser.ArgListToDictAction,
        nargs="+",
        default={},
        type=parser.split_argument,
        required=False,
        help="Variables that will interpolated into the settings files."
        )

    # TODO: add version parameter

    return parser


# --------------------------------------------------------------------------- #
def main(_cli_runner_factory=CliRunner):

    cli = _cli_runner_factory(
        sys.argv[1:],
        configured_argument_parser(),
        PACKAGE_LOGGER_NAME,
        sys.stdout,
        sys.stderr)

    return cli.run()
