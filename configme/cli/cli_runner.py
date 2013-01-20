# -*- coding: utf-8 -*-

"""
CLI Module
"""

import sys

from .cli_logger import cli_logger_factory
from ..config import Configurator
from ..role import Role
from ..exceptions import ConfigMeException


# --------------------------------------------------------------------------- #
class CliRunner(object):

    logger = None

    _script_args = None

    _configurator_factory = None
    _role_factory = None

    _last_exception = None

    # ....................................................................... #
    def __init__(self,
                 script_args,
                 argument_parser,
                 logger_name,
                 logger_out,
                 loggerr_err,
                 _logger_factory=cli_logger_factory,
                 _configurator_factory=Configurator,
                 _role_factory=Role):
        """
        Main entry point for the CLI script.
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

        :type _script_args: tuple/list
        """

        self._logger_factory = _logger_factory
        self._argument_parser = argument_parser
        self._configurator_factory = _configurator_factory
        self._role_factory = _role_factory

        self._script_args = script_args
        self._logger_name = logger_name
        self._logger_out = logger_out
        self._loggerr_err = loggerr_err

    # ....................................................................... #
    def run(self):
        """
        Run config generation.

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

        :return: 0 on success, 1 on a known error, 2 on unknown error or fatal
                 error.
        :rtype: int
        """
        output_list = []
        return_code = 0

        # setup logging. catch everything here. Any error here and we are done
        try:
            self.logger = self._logger_factory(
                self._logger_name,
                self._logger_out,
                self._loggerr_err)
        except:
            message = "Fatal Error: could not even setup a basic logger.\n"
            sys.stderr.write(message)
            return 2

        #if True:
        try:
            # parse args
            parsed_args = self._argument_parser.parse(self._script_args)

            # setup config
            config = self._configurator_factory(
                templates_path=parsed_args.templates_path,
                settings_path=parsed_args.settings_path,
                output_path=parsed_args.output_path)

            # init role
            role = self._role_factory(
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
            self.logger.error("Error: %s" % err.message)
            return_code = 1
        except Exception as err:
            # handle any errors we do not recognize
            self.logger.error("Unknown Error: %s" % err.message)
            return_code = 2

        # log all the files and folders if any have been recorded
        for item in output_list:
            self.logger.info(item)

        return return_code
