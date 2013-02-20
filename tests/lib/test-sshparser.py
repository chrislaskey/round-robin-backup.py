# -*- coding: utf8 -*-

# nosetests --with-coverage --cover-package=lib.sshparser \
# --nocapture ./tests

from nose.tools import *
from lib.sshparser import SSHParser

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

