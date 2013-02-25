# -*- coding: utf8 -*-

# nosetests --with-coverage --cover-package=roundrobinbackupoptionsparser \
# --nocapture ./tests

import sys
from nose.tools import *
from tests.utils import no_stdout_or_stderr
from lib.optionsparser import ArgParser

# def no_stdout_or_stderr(func):
#     '''
#     Blocks stdout and stderr from being displayed. It will not block Nose
#     errors, Python exceptions, etc. Useful for functions that automatically
#     write to the command line, like argparse.

#     Need to use additional functools.wraps decorator for Nose to recongize
#     custom decorators. See: http://stackoverflow.com/questions/7727678/
#     '''
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         self.stdout = sys.stdout
#         self.stderr = sys.stderr
#         sys.stderr = open(os.devnull, "w")
#         sys.stdout = open(os.devnull, "w")
#         func(self, *args, **kwargs)
#         sys.stdout = self.stdout
#         sys.stderr = self.stderr
#     return wrapper

class TestArgParser:

    def setup(self):
        "Set up test fixtures"
        self.args_parser = ArgParser()

    def teardown(self):
        "Tear down test fixtures"

    def set_command_line_arguments(self, new_value_list):
        sys.argv = ['./roundrobinbackup.py'] + new_value_list

    @no_stdout_or_stderr
    def test_no_arguments_raises_error(self):
        self.set_command_line_arguments([])
        assert_raises(SystemExit, self.args_parser.get_args)

    @no_stdout_or_stderr
    def test_missing_target_arguments_raises_error(self):
        self.set_command_line_arguments(['user@target.com:/path'])
        assert_raises(SystemExit, self.args_parser.get_args)

    @no_stdout_or_stderr
    def test_missing_destination_arguments_raises_error(self):
        self.set_command_line_arguments(['/local/files'])
        assert_raises(SystemExit, self.args_parser.get_args)

    def test_required_arguments_return_as_expected(self):
        arguments = [
            '/local/files',
            'user@target.com:/path'
        ]
        self.set_command_line_arguments(arguments)

        returned = self.args_parser.get_args()
        assert_equal(returned['source'], '/local/files')
        assert_equal(returned['destination'], 'user@target.com:/path')

    def test_required_arguments_return_default_optional_argument_values_as_expected(self):
        arguments = [
            '/local/files',
            'user@target.com:/path'
        ]
        self.set_command_line_arguments(arguments)

        returned = self.args_parser.get_args()
        assert_equal(returned['source'], '/local/files')
        assert_equal(returned['destination'], 'user@target.com:/path')
        assert_equal(returned['debug'], False)
        assert_equal(returned['exclude'], [])
        assert_equal(returned['ssh_identity_file'], None)
        assert_equal(returned['ssh_port'], '22')
        assert_equal(returned['days'], '6')
        assert_equal(returned['weeks'], '5')
        assert_equal(returned['months'], '6')
        assert_equal(returned['years'], '10')
        assert_equal(returned['rsync_dir'], 'latest')
        assert_equal(returned['backup_prefix'], 'automated-backup-')

    @no_stdout_or_stderr
    def test_invalid_argument_raises_error(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--invalid-option'
        ]
        self.set_command_line_arguments(arguments)
        assert_raises(SystemExit, self.args_parser.get_args)

    @no_stdout_or_stderr
    def test_empty_excludes_argument_raises_error(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--exclude'
        ]
        self.set_command_line_arguments(arguments)
        assert_raises(SystemExit, self.args_parser.get_args)

    def test_one_excludes_argument_returns_as_expected(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--exclude',
            '.git/*',
        ]
        self.set_command_line_arguments(arguments)
        returned = self.args_parser.get_args()
        assert_equal(returned['source'], '/local/files')
        assert_equal(returned['destination'], 'user@target.com:/path')
        assert_equal(returned['exclude'], ['.git/*'])

    def test_multiple_excludes_argument_returns_as_expected(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--exclude',
            '.git/*',
            '--exclude',
            '.venv/*',
        ]
        self.set_command_line_arguments(arguments)
        returned = self.args_parser.get_args()
        assert_equal(returned['source'], '/local/files')
        assert_equal(returned['destination'], 'user@target.com:/path')
        assert_equal(returned['exclude'], ['.git/*', '.venv/*'])

    @no_stdout_or_stderr
    def test_empty_identity_file_argument_raises_error(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--ssh-identity-file'
        ]
        self.set_command_line_arguments(arguments)
        assert_raises(SystemExit, self.args_parser.get_args)

    @no_stdout_or_stderr
    def test_invalid_identity_file_argument_returns_as_expected(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--ssh-identity-file',
            '/file/does/not/exist',
        ]
        self.set_command_line_arguments(arguments)
        assert_raises(Exception, self.args_parser.get_args)

    def test_identity_file_argument_returns_as_expected(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--ssh-identity-file',
            '/dev/null',
        ]
        self.set_command_line_arguments(arguments)
        returned = self.args_parser.get_args()
        assert_equal(returned['ssh_identity_file'], '/dev/null')

    def test_no_ssh_port_argument_returns_default(self):
        arguments = [
            '/local/files',
            'user@target.com:/path'
        ]
        self.set_command_line_arguments(arguments)
        returned = self.args_parser.get_args()
        assert_equal(returned['ssh_port'], '22')

    @no_stdout_or_stderr
    def test_empty_ssh_port_argument_raises_error(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--ssh-port'
        ]
        self.set_command_line_arguments(arguments)
        assert_raises(SystemExit, self.args_parser.get_args)

    def test_ssh_port_argument_returns_as_expected(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--ssh-port',
            '2222'
        ]
        self.set_command_line_arguments(arguments)
        returned = self.args_parser.get_args()
        assert_equal(returned['ssh_port'], '2222')

    @no_stdout_or_stderr
    def test_empty_days_argument_raises_error(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--days'
        ]
        self.set_command_line_arguments(arguments)
        assert_raises(SystemExit, self.args_parser.get_args)

    def test_days_argument_returns_as_expected(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--days',
            '55'
        ]
        self.set_command_line_arguments(arguments)
        returned = self.args_parser.get_args()
        assert_equal(returned['days'], '55')

    @no_stdout_or_stderr
    def test_empty_weeks_argument_raises_error(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--weeks'
        ]
        self.set_command_line_arguments(arguments)
        assert_raises(SystemExit, self.args_parser.get_args)

    def test_weeks_argument_returns_as_expected(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--weeks',
            '11'
        ]
        self.set_command_line_arguments(arguments)
        returned = self.args_parser.get_args()
        assert_equal(returned['weeks'], '11')

    @no_stdout_or_stderr
    def test_empty_months_argument_raises_error(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--months'
        ]
        self.set_command_line_arguments(arguments)
        assert_raises(SystemExit, self.args_parser.get_args)

    def test_months_argument_returns_as_expected(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--months',
            '8'
        ]
        self.set_command_line_arguments(arguments)
        returned = self.args_parser.get_args()
        assert_equal(returned['months'], '8')

    @no_stdout_or_stderr
    def test_empty_years_argument_raises_error(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--years'
        ]
        self.set_command_line_arguments(arguments)
        assert_raises(SystemExit, self.args_parser.get_args)

    def test_years_argument_returns_as_expected(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--years',
            '8'
        ]
        self.set_command_line_arguments(arguments)
        returned = self.args_parser.get_args()
        assert_equal(returned['years'], '8')


    @no_stdout_or_stderr
    def test_rsync_dir_prefix_argument_raises_error(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--rsync-dir'
        ]
        self.set_command_line_arguments(arguments)
        assert_raises(SystemExit, self.args_parser.get_args)

    def test_rsync_dir_argument_returns_as_expected(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--rsync-dir',
            'live-files'
        ]
        self.set_command_line_arguments(arguments)
        returned = self.args_parser.get_args()
        assert_equal(returned['rsync_dir'], 'live-files')

    @no_stdout_or_stderr
    def test_empty_backup_prefix_argument_raises_error(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--backup-prefix'
        ]
        self.set_command_line_arguments(arguments)
        assert_raises(SystemExit, self.args_parser.get_args)

    def test_backup_prefix_argument_returns_as_expected(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--backup-prefix',
            'rrbackup'
        ]
        self.set_command_line_arguments(arguments)
        returned = self.args_parser.get_args()
        assert_equal(returned['backup_prefix'], 'rrbackup')

    def test_all_arguments_return_as_expected(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--debug',
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
        returned = self.args_parser.get_args()
        assert_equal(returned['source'], '/local/files')
        assert_equal(returned['destination'], 'user@target.com:/path')
        assert_equal(returned['debug'], True)
        assert_equal(returned['exclude'], ['.git/*', '.venv/*'])
        assert_equal(returned['ssh_identity_file'], '/dev/null')
        assert_equal(returned['ssh_port'], '2222')
        assert_equal(returned['days'], '5')
        assert_equal(returned['weeks'], '4')
        assert_equal(returned['months'], '3')
        assert_equal(returned['years'], '2')
        assert_equal(returned['rsync_dir'], 'live-files')
        assert_equal(returned['backup_prefix'], 'rrbackup')
