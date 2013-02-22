# -*- coding: utf8 -*-

# nosetests --with-coverage --cover-package=roundrobinbackupoptionsparser \
# --nocapture ./tests

import sys
from nose.tools import *
from tests.mocksandstubs import CommandLineMock
from tests.utils import no_stdout_or_stderr
from roundrobinbackup import RoundRobinBackup

class TestRoundRobinBackup:

    def setup(self):
        "Set up test fixtures"

    def teardown(self):
        "Tear down test fixtures"
    
    def set_command_line_arguments(self, new_value_list):
        sys.argv = ['./roundrobinbackup.py'] + new_value_list

    def test_minimum_options_return_expected_default_values(self):
        arguments = [
            '/local/files',
            'user@target.com:/some/path'
        ]
        self.set_command_line_arguments(arguments)
        rrbackup = RoundRobinBackup()

        returned = rrbackup.get_options()
        assert_equal(returned['source'], '/local/files')
        assert_equal(returned['destination'], 'user@target.com:/some/path')
        assert_equal(returned['destination_user'], 'user')
        assert_equal(returned['destination_host'], 'target.com')
        assert_equal(returned['destination_path'], '/some/path')
        assert_equal(returned['exclude'], [])
        assert_equal(returned['ssh_identity_file'], None)
        assert_equal(returned['ssh_port'], '22')
        assert_equal(returned['rsync_dir'], 'latest')
        assert_equal(returned['backup_prefix'], 'automated-backup-')

    @no_stdout_or_stderr
    def test_missing_command_line_args_raises_error(self):
        arguments = []
        self.set_command_line_arguments(arguments)
        # Object instantiation will throw a SystemExit since the init method
        # calls methods that parse the command line arguments.
        assert_raises(SystemExit, RoundRobinBackup)

    def test_custom_options_return_as_expected(self):
        arguments = [
            '/local/files',
            'user@target.com:/some/path',
            '--exclude',
            '.git/*',
            '--exclude',
            '.venv/*',
            '--ssh-identity-file',
            '/dev/null',
            '--ssh-port',
            '2222',
            '--days',
            '5',
            '--weeks',
            '4',
            '--months',
            '3',
            '--years',
            '2',
            '--rsync-dir',
            'live-files',
            '--backup-prefix',
            'rrbackup'
        ]
        self.set_command_line_arguments(arguments)
        rrbackup = RoundRobinBackup()

        returned = rrbackup.get_options()
        assert_equal(returned['source'], '/local/files')
        assert_equal(returned['destination'], 'user@target.com:/some/path')
        assert_equal(returned['destination_user'], 'user')
        assert_equal(returned['destination_host'], 'target.com')
        assert_equal(returned['destination_path'], '/some/path')
        assert_equal(returned['exclude'], ['.git/*', '.venv/*'])
        assert_equal(returned['ssh_identity_file'], '/dev/null')
        assert_equal(returned['ssh_port'], '2222')
        assert_equal(returned['days'], '5')
        assert_equal(returned['weeks'], '4')
        assert_equal(returned['months'], '3')
        assert_equal(returned['years'], '2')
        assert_equal(returned['rsync_dir'], 'live-files')
        assert_equal(returned['backup_prefix'], 'rrbackup')

    def test_no_archives_exist(self):
        arguments = [
            '/local/files',
            'user@target.com:/some/path'
        ]
        self.set_command_line_arguments(arguments)

        cli_input_output = [
            ('ssh user@target.com /bin/mkdir -p /some/path/latest', ''),
            ('rsync -avz -e ssh /local/files user@target.com:/some/path/latest', ''),
            ('ssh user@target.com /bin/ls /some/path', '')
        ]
        cli_mock = CommandLineMock(cli_input_output)
        rrbackup = RoundRobinBackup()
        rrbackup.set_command_line_library(cli_mock)
        rrbackup.backup()

    def test_archives_exist(self):
        arguments = [
            '/local/files',
            'user@target.com:/some/path'
        ]
        self.set_command_line_arguments(arguments)

        # Oldest date will be used as an anchor. The second date does not line
        # up with the anchor date, and should be requested to be removed,
        # generating the last command in cli_input_output.
        existing_backup_files = [
            'automated-backup-1996-01-21',
            'automated-backup-2004-02-21',
            'automated-backup-2004-02-22'
        ]
        existing_backups = '\n'.join(existing_backup_files)
        cli_input_output = [
            ('ssh user@target.com /bin/mkdir -p /some/path/latest', ''),
            ('rsync -avz -e ssh /local/files user@target.com:/some/path/latest', ''),
            ('ssh user@target.com /bin/ls /some/path', existing_backups),
            ('ssh user@target.com /bin/rm -r /some/path/automated-backup-2004-02-21 /some/path/automated-backup-2004-02-22', '')
        ]
        cli_mock = CommandLineMock(cli_input_output)
        rrbackup = RoundRobinBackup()
        rrbackup.set_command_line_library(cli_mock)
        rrbackup.backup()
