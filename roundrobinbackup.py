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
        self._create_backup()
        self._create_archive()
        self._remove_stale_archives()

    def _create_backup(self):
        creator = self._create_backup_agent('creator')
        creator.sync_files()

    def _create_backup_agent(self, type):
        agent = self._backup_agent_simple_factory(type)
        agent.set_options(self.options)
        agent.set_command_line_library(self.command_line_library)
        return agent

    def _backup_agent_simple_factory(self, type):
        if type == 'creator':
            agent = BackupCreator()
        elif type == 'archiver':
            agent = BackupArchiver()
        elif type == 'archive_pruner':
            agent = BackupArchivePruner()
        return agent

    def _create_archive(self):
        archiver = self._create_backup_agent('archiver')
        archiver.create()

    def _remove_stale_archives(self):
        archive_pruner = self._create_backup_agent('archive_pruner')
        archive_pruner.cleanup_backups()

if __name__ == "__main__":
    RoundRobinBackup().backup()
