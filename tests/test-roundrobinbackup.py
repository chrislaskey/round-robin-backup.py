# -*- coding: utf8 -*-

# nosetests --with-coverage --cover-package=<package> \
# --nocapture ./tests

import sys
from nose.tools import *
from tests.mocksandstubs import CommandLineMock
from tests.utils import no_stdout_or_stderr
from utilities.roundrobindate import RoundRobinDate
from roundrobinbackup import RoundRobinBackup


class TestRoundRobinBackup:

    def setup(self):
        "Set up test fixtures"
        todays_date = RoundRobinDate().get_today()
        self.today = todays_date

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

    def test_full_execution_when_no_remote_archives_exist(self):
        arguments = [
            '/local/files',
            'user@target.com:/some/path'
        ]
        self.set_command_line_arguments(arguments)

        cli_input_output = [
            ('ssh user@target.com /bin/mkdir -p /some/path/latest', ''),
            ('rsync -avz --delete -e ssh /local/files user@target.com:/some/path/latest', ''),
            ('ssh user@target.com /bin/tar -C /some/path -cjf /some/path/automated-backup-{0}.tar.bzip2 latest'.format(self.today), ''),
            ('ssh user@target.com /bin/ls /some/path', '')
        ]
        cli_mock = CommandLineMock(cli_input_output)
        rrbackup = RoundRobinBackup()
        rrbackup.set_command_line_library(cli_mock)
        rrbackup.backup()

    def test_full_execution_when_remote_archives_exist(self):
        arguments = [
            '/local/files',
            'user@target.com:/some/path'
        ]
        self.set_command_line_arguments(arguments)

        # Oldest date will be used as an anchor. The second date does not line
        # up with the anchor date, and should be requested to be removed,
        # generating the last command in cli_input_output.
        existing_backup_files = [ # Note file's extension doesn't matter
            'automated-backup-1996-01-21',
            'automated-backup-2004-02-21.tar.bzip2',
            'automated-backup-2004-02-22.tar'
        ]
        existing_backups = '\n'.join(existing_backup_files)
        cli_input_output = [
            ('ssh user@target.com /bin/mkdir -p /some/path/latest', ''),
            ('rsync -avz --delete -e ssh /local/files user@target.com:/some/path/latest', ''),
            ('ssh user@target.com /bin/tar -C /some/path -cjf /some/path/automated-backup-{0}.tar.bzip2 latest'.format(self.today), ''),
            ('ssh user@target.com /bin/ls /some/path', existing_backups),
            ('ssh user@target.com /bin/rm -r /some/path/automated-backup-2004-02-21.tar.bzip2 /some/path/automated-backup-2004-02-22.tar', '')
        ]
        cli_mock = CommandLineMock(cli_input_output)
        rrbackup = RoundRobinBackup()
        rrbackup.set_command_line_library(cli_mock)
        rrbackup.backup()

    def test_full_execution_with_options_when_remote_archives_exist(self):
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

        existing_backup_files = [ # Note file's extension doesn't matter
            'rrbackup1996-01-21',
            'rrbackup2004-02-21.tar.bzip2',
            'rrbackup2004-02-22.tar'
        ]
        existing_backups = '\n'.join(existing_backup_files)
        cli_input_output = [
            ('ssh user@target.com -p 2222 -i /dev/null /bin/mkdir -p /some/path/live-files', ''),
            ('rsync -avz --delete -e ssh -p 2222 -i /dev/null /local/files user@target.com:/some/path/live-files --exclude .git/* --exclude .venv/*', ''),
            ('ssh user@target.com -p 2222 -i /dev/null /bin/tar -C /some/path -cjf /some/path/rrbackup{0}.tar.bzip2 live-files'.format(self.today), ''),
            ('ssh user@target.com -p 2222 -i /dev/null /bin/ls /some/path', existing_backups),
            ('ssh user@target.com -p 2222 -i /dev/null /bin/rm -r /some/path/rrbackup2004-02-21.tar.bzip2 /some/path/rrbackup2004-02-22.tar', '')
        ]
        cli_mock = CommandLineMock(cli_input_output)
        rrbackup = RoundRobinBackup()
        rrbackup.set_command_line_library(cli_mock)
        rrbackup.backup()
