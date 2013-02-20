#!/usr/bin/env python

import argparse
import textwrap
from lib.commandline import CommandLine
from lib.roundrobindate import RoundRobinDate
from lib.sshparser import SSHParser

class RoundRobinBackup:

    def __init__(self):
        self._set_options()
        self._set_date_library()
        self._set_command_line_library()

    def _set_options(self):
        parser = RoundRobinBackupOptionsParser()
        options = parser.get_options()
        self.options = options

    def get_options(self):
        return self.options.copy()

    def _set_date_library(self):
        # TODO add day, week, month, year options
        date_library = RoundRobinDate()
        self.date_generator = date_library

    def _set_command_line_library(self):
        command_line_library = CommandLine()
        self.command_line_library = command_line_library

    def backup(self):
        self._remote_sync()
        self._remote_archive()
        self._remote_cleanup()

    def _remote_sync(self):
        sync = RoundRobinBackupRemoteSync()
        sync.set_command_line_library(self.command_line_library)
        sync.sync_files()

    def _remote_archive(self):
        archive = RoundRobinBackupRemoteArchive()
        archive.set_command_line_library(self.command_line_library)
        archive.create_archive()

    def _remote_cleanup(self):
        cleanup = RoundRobinBackupRemoteCleanup()
        cleanup.set_command_line_library(self.command_line_library)
        cleanup.set_date_generator()
        cleanup.remote_stale_backups()

class RoundRobinBackupOptionsParser:

    def get_options(self):
        self.args = self._get_args()
        options = self._parse_args_and_return_options()
        return options

    def _get_args(self):
        parser = RoundRobinBackupCommandLineArgsParser()
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
        parsed = self._flatten_excludes_list(parsed)
        return parsed

    def _flatten_excludes_list(self, parsed):
        if parsed.exclude:
            nested_list = parsed.exclude
            flattened = [item for sublist in nested_list for item in sublist]
            parsed.exclude = flattened
        else:
            parsed.exclude = []
        return parsed

class AbstractRoundRobinBackupActions:

    def set_options(self, options):
        self.options = options

    def set_command_line_library(self, command_line_library):
        self.cli = command_line_library

class RoundRobinBackupRemoteSync(AbstractRoundRobinBackupActions):

    def __init__(self, options):
        self.options = options
        # Create backup dir if needed
        # rsync data

    def create_backup_dir(self):
        pass

class RoundRobinBackupRemoteArchive(AbstractRoundRobinBackupActions):

    def __init__(self, options):
        self.options = options
        # Create today's archive dir
        # Use live backup dir to tar+bzip2 files

class RoundRobinBackupRemoteCleanup(AbstractRoundRobinBackupActions):

    def __init__(self, options):
        self.options = options
        # Get all existing rrbackup dirs
        # Remove ones that don't fit the date

if __name__ == "__main__":
    RoundRobinBackup()
