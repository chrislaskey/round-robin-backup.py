#!/usr/bin/env python

from lib.optionsparser import OptionsParser
from lib.backupcreator import BackupCreator
from lib.backuparchiver import BackupArchiver
from lib.backuparchivepruner import BackupArchivePruner
from utilities.commandline import CommandLine


class RoundRobinBackup:

    def __init__(self):
        self._set_options()
        self._set_default_command_line_library()

    def _set_options(self):
        parser = OptionsParser()
        options = parser.get_options()
        self.options = options

    def get_options(self):
        return self.options.copy()

    def _set_default_command_line_library(self):
        if self.options['debug']:
            from tests.mocksandstubs import CommandLineStubPrinter
            command_line_library = CommandLineStubPrinter()
        else:
            command_line_library = CommandLine()
        self.set_command_line_library(command_line_library)

    def set_command_line_library(self, command_line_library):
        self.command_line_library = command_line_library

    def backup(self):
        self._execute('backup')
        self._execute('archive')
        self._execute('cleanup')

    def _execute(self, type):
        agent = self._backup_agent_simple_factory(type)
        agent.set_options(self.options)
        agent.set_command_line_library(self.command_line_library)
        agent.execute()

    def _backup_agent_simple_factory(self, type):
        if type == 'backup':
            agent = BackupCreator()
        elif type == 'archive':
            agent = BackupArchiver()
        elif type == 'cleanup':
            agent = BackupArchivePruner()
        return agent

if __name__ == "__main__":
    RoundRobinBackup().backup()
