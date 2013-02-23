# -*- coding: utf8 -*-

# nosetests --with-coverage --cover-package=lib.optionsparser \
# --nocapture ./tests/lib

import sys
from nose.tools import *
from lib.optionsparser import OptionsParser

class TestOptionsParser:

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
        self.options_parser = OptionsParser()

        returned = self.options_parser.get_options()
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
        self.options_parser = OptionsParser()

        returned = self.options_parser.get_options()
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
