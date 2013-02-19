# -*- coding: utf8 -*-

# nosetests --with-coverage --cover-package=roundrobinbackupoptionsparser --nocapture ./tests

from nose.tools import *
from roundrobinbackup import RoundRobinBackupOptionsParser
from datetime import date

class TestRoundRobinDateOptionsParser():

    def setup(self):
        "Set up test fixtures"
        self.options_parser = RoundRobinBackupOptionsParser()

    def teardown(self):
        "Tear down test fixtures"

