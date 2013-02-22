import argparse
import textwrap
import os
from utilities.sshutilities import SSHParser

class OptionsParser:

    def get_options(self):
        self.args = self._get_args()
        options = self._parse_args_and_return_options()
        return options

    def _get_args(self):
        parser = ArgParser()
        args = parser.get_args()
        return args

    def _parse_args_and_return_options(self):
        options = self.args.copy()
        destination_options = self._create_destination_options()
        options.update(destination_options)
        return options

    def _create_destination_options(self):
        ssh_parser = SSHParser()
        ssh_string = self.args['destination']
        parsed = ssh_parser.parse(ssh_string)
        new_destination_options = {
            'destination_user': parsed['user'],
            'destination_host': parsed['host'],
            'destination_path': parsed['path'],
        }
        return new_destination_options

class ArgParser:

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
        required = parser.add_argument_group('Required Arguments')
        required.add_argument('source',
            help='The source directory path'
        )
        required.add_argument('destination',
            help='The target destination, in rsync/ssh compatible format:\
                  user@example.com:/absolute/path/to/backup/dir'
        )
        return parser

    def _add_optional_rsync_argparse_arguments(self, parser):
        configuration = parser.add_argument_group('Configuration options')
        configuration.add_argument('-p', '--ssh-port',
            action='store',
            default='22',
            help='Specify a remote SSH port (defaults to port 22)'
        )
        configuration.add_argument('-i', '--ssh-identity-file',
            action='store',
            help='Specify a SSH Identity file'
        )
        configuration.add_argument('-E', '--exclude',
            action='append',
            nargs='+',
            help='Specify a file or directory to exclude from rsync. Can be \
                  declared multiple times'
        )
        configuration.add_argument('--rsync-dir',
            action='store',
            default='latest',
            help='Directory within destination to keep the latest unzipped \
                  rsync files'
        )
        configuration.add_argument('--backup-prefix',
            action='store',
            default='automated-backup-',
            help='Prefix of backup.tar.bzip2 files, e.g. \
                  <backup-prefix>-<date>.tar.bzip2'
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
        parsed = self._convert_identity_file_to_absolute_path(parsed)
        parsed = self._flatten_excludes_list(parsed)
        return parsed

    def _convert_identity_file_to_absolute_path(self, parsed):
        if parsed.ssh_identity_file:
            absolute_file = os.path.abspath(parsed.ssh_identity_file)
            if not os.path.exists(absolute_file):
                raise Exception("Invalid SSH identity file, "
                    "'{0}'".format(absolute_file))
            parsed.ssh_identity_file = absolute_file
        return parsed

    def _flatten_excludes_list(self, parsed):
        if parsed.exclude:
            nested_list = parsed.exclude
            flattened = [item for sublist in nested_list for item in sublist]
            parsed.exclude = flattened
        else:
            parsed.exclude = []
        return parsed

