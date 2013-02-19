#!/usr/bin/env python

import argparse
import textwrap
from lib.commandline import CommandLine
from lib.roundrobindate import RoundRobinDate

class RoundRobinBackup:

    def __init__(self):
        self._set_options()

    def _set_options(self):
        command_line_parser = RoundRobinBackupCommandLineArgsParser()
        command_line_args = command_line_parser.get_args()
        self.options = command_line_args

    def get_options(self):
        return self.options.copy()

    def set_date_generator(self, date_generator):
        pass

    def set_command_line_library(self, command_line_library):
        pass

    def return_dates(self):
        pass

    def execute_command(self):
        pass

class RoundRobinBackupCommandLineArgsParser:

    def get_args(self):
        parsed = self._parse()
        processed = self._process(parsed)
        args_dict = vars(processed)
        return args_dict

    def _parse(self):
        argparse_options = self._get_argparse_options()
        parser = argparse.ArgumentParser(**argparse_options)
        parser = self._add_required_argparse_arguments(parser)
        parser = self._add_optional_rsync_argparse_arguments(parser)
        parser = self._add_optional_date_argparse_arguments(parser)
        parsed = parser.parse_args()
        return parsed

    def _get_argparse_options(self):
        options = {
            'formatter_class': argparse.RawDescriptionHelpFormatter,
            'description': self._get_argparse_preface(),
            'epilog': self._get_argparse_epilogue()
        }
        return options
    
    def _get_argparse_preface(self):
        preface = textwrap.dedent('''
            ABOUT

            COMMANDS

            ''')
        return preface

    def _get_argparse_epilogue(self):
        epilog = textwrap.dedent('''
            EPILOG

            For more technical documentation, see the README.md file or visit
            the project page on github:

            http://github.com/chrislaskey/round-robin-backup.py
            ''')
        return epilog

    def _add_required_argparse_arguments(self, parser):
        import_required = parser.add_argument_group('Required Arguments')
        import_required.add_argument('source',
            help='The source directory path'
        )
        import_required.add_argument('destination',
            help='The target destination, in rsync/ssh compatible format:\
                  user@example.com:/absolute/path/to/target/destination'
        )
        return parser

    def _add_optional_rsync_argparse_arguments(self, parser):
        rsync_options = parser.add_argument_group('Configuration options')
        rsync_options.add_argument('-p', '--ssh-port',
            action='store',
            default='22',
            help='Specify a remote SSH port (defaults to port 22)'
        )
        rsync_options.add_argument('-i', '--ssh-identity-file',
            action='store',
            help='Specify a SSH Identity file'
        )
        rsync_options.add_argument('-E', '--exclude',
            action='append',
            nargs='+',
            help='Specify a file or directory to exclude from rsync. Can be \
                  declared multiple times'
        )
        return parser

    def _add_optional_date_argparse_arguments(self, parser):
        date_options = parser.add_argument_group('Configuration options')
        date_options.add_argument('--days',
            action='store',
            default='6',
            help='Specify number of days to retain. Default is 6 \
                 (does not include current day)'
        )
        date_options.add_argument('--weeks',
            action='store',
            default='5',
            help='Specify number of weeks to retain. Default is 5'
        )
        date_options.add_argument('--months',
            action='store',
            default='6',
            help='Specify number of months to retain. Default is 6'
        )
        date_options.add_argument('--years',
            action='store',
            default='10',
            help='Specify number of years to retain. Default is 10'
        )
        return parser

    def _process(self, parsed):
        if parsed.exclude:
            parsed.exclude = self._flatten_excludes_list(parsed.exclude)
        else:
            parsed.exclude = []
        return parsed

    def _flatten_excludes_list(self, nested_list):
        flattened = [item for sublist in nested_list for item in sublist]
        return flattened

if __name__ == "__main__":
    RoundRobinBackup()
