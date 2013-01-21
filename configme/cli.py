# -*- coding: utf-8 -*-
# package

import sys

from logging import CRITICAL
from logging import DEBUG
from logging import ERROR
from logging import INFO
from logging import WARNING

from logging import getLogger
from logging import StreamHandler

from .cli_argparse import CliArgumentParser
from .config import Configurator
from .exceptions import ConfigMeException
from .role import Role
from .utils import AllowedLevelsFilter

from .package_info import PACKAGE_NAME
from .package_info import PACKAGE_VERSION_FULL
from .package_info import PACKAGE_LOGGER_NAME


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
    # TODO: figure out how to handle "--help/-h", as it now throws an error

    return parser


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

    logger_ = getLogger(name)
    logger_.setLevel(DEBUG)

    # handles DEBUG and INFO
    handler_out = StreamHandler(out)
    level_filter = AllowedLevelsFilter([DEBUG, INFO])
    handler_out.addFilter(level_filter)
    logger_.addHandler(handler_out)

    # handles WARNING, ERROR, and CRITICAL
    handler_err = StreamHandler(err)
    level_filter = AllowedLevelsFilter([WARNING, ERROR, CRITICAL])

    handler_err.addFilter(level_filter)
    logger_.addHandler(handler_err)

    return logger_


# --------------------------------------------------------------------------- #
def cli_run(
    script_args,
    argument_parser,
    logger_name,
    logger_out,
    logger_err,
    _logger_factory=cli_logger_factory,
    _configurator_factory=Configurator,
    _role_factory=Role
):
    """
    Run CLI config generation.

    Parses arguments from the command line and run role generation.

    :param script_args:

        script arguments, basically sysv but without the first argument of
        script name.

        script arguments as a list or a tuple, in the same format as
        sys.argv but without the script name as the script name as the
        first element. The arguments should include:

            - templates_path - templates path, required.
            - settings_path - settings path, required.
            - output_path - output path, required.
            - role_name - role name, required.
            - role_suffix - role suffix, optional.
            - role_variables - role variables, optional.

    :type script_args: list/tuple of sysv style arguments

    :param argument_parser:

        instance of CliArgumentParser with configured parameters.

    :type argument_parser: :class:`CliArgumentParser`

    :param logger_name: name of the logger to be used.
    :type logger_name: str/unicode

    :param logger_out: stream to log output to.
    :type logger_out: stream

    :param logger_err: stream to log errors to.
    :type logger_err: stream


    :return:

        In case of success:

        - Write out list files generated files, one file per line.
          The path of the file is relative to the given --output-path

        - return 0

        In case of known error:

        - Write out 'Error: ' followed by the error message to the error
          file descriptor. Follow up by writing out the list of files if
          any were generated to the out file out. Then exit with return
          code of 1

        In case of unknown error:

        - write out 'Unknown Error: ' error file descriptor followed by the
          error message. and exit with return code of 2

        In case of not being able to setup the basic CLI logger:

        - write out "Fatal: could not even setup a basic logger." to stderr
          and exit with return code of 2

    :rtype: int
    """

    output_list = []
    return_code = 0

    # setup logging. catch everything here. Any error here and we are done
    try:
        logger = _logger_factory(
            name=logger_name,
            out=logger_out,
            err=logger_err)
    except:
        message = "Fatal Error: could not even setup a basic logger.\n"
        sys.stderr.write(message)
        return 2

    #if True:
    try:
        # parse args
        parsed_args = argument_parser.parse(script_args)

        # setup config
        config = _configurator_factory(
            templates_path=parsed_args.templates_path,
            settings_path=parsed_args.settings_path,
            output_path=parsed_args.output_path)

        # init role
        role = _role_factory(
            config=config,
            name=parsed_args.role_name,
            suffix=parsed_args.role_suffix,
            variables=parsed_args.role_variables)

        # and write config files out
        output_list = role.write_configs()
    #try:
    #    pass
    except ConfigMeException as err:
        # handle any recognizable erros in a CLI friendly fashion
        logger.error("Error: %s" % err.message)
        return_code = 1
    except Exception as err:
        # handle any errors we do not recognize
        logger.error("Unknown Error: %s" % err.message)
        return_code = 2

    # log all the files and folders if any have been recorded
    for item in output_list:
        logger.info(item)

    return return_code


# --------------------------------------------------------------------------- #
def main(_cli_run=cli_run):

    return _cli_run(
        sys.argv[1:],
        configured_argument_parser(),
        PACKAGE_LOGGER_NAME,
        sys.stdout,
        sys.stderr)
