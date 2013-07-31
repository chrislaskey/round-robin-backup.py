# -*- coding: utf8 -*-

# nosetests --with-coverage --cover-package=lib.sshparser \
# --nocapture ./tests

from nose.tools import *
from utilities.sshutilities import SSHCommand, SSHParser


class TestSSHCommand:

    def setup(self):
        "Set up test fixtures"
        self.command = SSHCommand()

    def teardown(self):
        "Tear down test fixtures"

    def test_simple(self):
        options = {
            'user': 'myuser',
            'host': 'example.com',
        }
        result = self.command.create(options)
        expected = ['ssh', 'myuser@example.com']
        assert_equal(result, expected)

    def test_host_only(self):
        options = {
            'host': 'example.com',
        }
        result = self.command.create(options)
        expected = ['ssh', 'example.com']
        assert_equal(result, expected)

    def test_with_user_and_host_omitted(self):
        ''' Useful in `rsync -e "ssh ..."` commands '''
        options = {
            'port': '2222',
        }
        result = self.command.create(options)
        expected = ['ssh', '-p', '2222']
        assert_equal(result, expected)

    def test_with_port_option(self):
        options = {
            'user': 'myuser',
            'host': 'example.com',
            'port': '2222',
        }
        result = self.command.create(options)
        expected = ['ssh', 'myuser@example.com', '-p', '2222']
        assert_equal(result, expected)

    def test_with_identity_file_option(self):
        options = {
            'user': 'myuser',
            'host': 'example.com',
            'port': '2222',
            'identity_file': '/path/to/file',
        }
        result = self.command.create(options)
        expected = ['ssh', 'myuser@example.com', '-p', '2222', '-i',
                    '/path/to/file']
        assert_equal(result, expected)

    def test_with_subcommand_option(self):
        options = {
            'user': 'myuser',
            'host': 'example.com',
            'subcommand': 'ls -la'
        }
        result = self.command.create(options)
        expected = ['ssh', 'myuser@example.com', 'ls -la']
        assert_equal(result, expected)

    def test_with_all_options(self):
        options = {
            'user': 'myuser',
            'host': 'example.com',
            'port': '2222',
            'identity_file': '/path/to/file',
            'subcommand': 'ls -la'
        }
        result = self.command.create(options)
        expected = ['ssh', 'myuser@example.com', '-p', '2222', '-i',
                    '/path/to/file', 'ls -la']
        assert_equal(result, expected)

    def test_string_return_with_all_options(self):
        options = {
            'user': 'myuser',
            'host': 'example.com',
            'port': '2222',
            'identity_file': '/path/to/file',
            'subcommand': 'ls -la'
        }
        result = self.command.create_command_string(options)
        expected = 'ssh myuser@example.com -p 2222 -i /path/to/file ls -la'
        assert_equal(result, expected)


class TestSSHParser:

    def setup(self):
        "Set up test fixtures"
        self.parser = SSHParser()

    def teardown(self):
        "Tear down test fixtures"

    def test_empty_string_returns_empty_pieces(self):
        input = ''
        result = self.parser.parse(input)
        expected = {
            'user': '',
            'host': '',
            'path': ''
        }
        assert_equal(result, expected)

    def test_simple_string_defaults_to_path_piece(self):
        input = '/some/test/path/string'
        result = self.parser.parse(input)
        expected = {
            'user': '',
            'host': '',
            'path': input
        }
        assert_equal(result, expected)

    def test_with_omitted_user(self):
        input = 'example.com:/some/path'
        result = self.parser.parse(input)
        expected = {
            'user': '',
            'host': 'example.com',
            'path': '/some/path'
        }
        assert_equal(result, expected)

    def test_with_full_string(self):
        input = 'myuser@example.com:/some/path'
        result = self.parser.parse(input)
        expected = {
            'user': 'myuser',
            'host': 'example.com',
            'path': '/some/path'
        }
        assert_equal(result, expected)
