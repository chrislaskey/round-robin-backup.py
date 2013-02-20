# -*- coding: utf8 -*-

# nosetests --with-coverage --cover-package=roundrobinbackupoptionsparser \
# --nocapture ./tests

import os
import sys
from nose.tools import *
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
            'user@target.com:/path'
        ]
        self.set_command_line_arguments(arguments)
        self.rrbackup = RoundRobinBackup()

        returned = self.rrbackup.get_options()
        assert_equal(returned['source'], '/local/files')
        assert_equal(returned['destination'], 'user@target.com:/path')
        assert_equal(returned['exclude'], [])
        assert_equal(returned['ssh_identity_file'], None)
        assert_equal(returned['ssh_port'], '22')

    def test_custom_options_return_as_expected(self):
        arguments = [
            '/local/files',
            'user@target.com:/path',
            '--exclude',
            '.git/*',
            '--exclude',
            '.venv/*',
            '--ssh-identity-file',
            '/path/to/ssh/identity/file',
            '--ssh-port',
            '2222'
        ]
        self.set_command_line_arguments(arguments)
        self.rrbackup = RoundRobinBackup()

        returned = self.rrbackup.get_options()
        assert_equal(returned['source'], '/local/files')
        assert_equal(returned['destination'], 'user@target.com:/path')
        assert_equal(returned['exclude'], ['.git/*', '.venv/*'])
        assert_equal(returned['ssh_identity_file'], '/path/to/ssh/identity/file')
        assert_equal(returned['ssh_port'], '2222')
