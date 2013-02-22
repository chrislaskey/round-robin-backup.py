#!/usr/bin/env python

from lib.optionsparser import OptionsParser
from lib.backupcreator import BackupCreator
from lib.backuparchiver import BackupArchiver
from lib.backuparchivepruner import BackupArchivePruner
from utilities.commandline import CommandLine

class RoundRobinBackup:

    def __init__(self):
        self._set_options()

    def _set_options(self):
        parser = OptionsParser()
        options = parser.get_options()
        self.options = options

    def get_options(self):
        return self.options.copy()

    def set_command_line_library(self, command_line_library):
        self.command_line_library = command_line_library

    def backup(self):
        self._create_backup()
        self._create_archive()
        self._remove_stale_archives()

    def _create_backup(self):
        creator = self._create_backup_actor('creator')
        creator.sync_files()

    def _create_backup_actor(self, type):
        backup = self._backup_actor_simple_factory(type)
        backup.set_options(self.options)
        backup.set_command_line_library(self.command_line_library)
        return backup

    def _backup_actor_simple_factory(self, type):
        if type == 'creator':
            backup = BackupCreator()
        elif type == 'archiver':
            backup = BackupArchiver()
        elif type == 'archive_pruner':
            backup = BackupArchivePruner()
        return backup

    def _create_archive(self):
        archiver = self._create_backup_actor('archiver')
        archiver.create()

    def _remove_stale_archives(self):
        archive_pruner = self._create_backup_actor('archive_pruner')
        archive_pruner.cleanup_backups()

if __name__ == "__main__":
    debug = True
    if debug:
        from tests.mocksandstubs import CommandLineStub
        command_line_library = CommandLineStub()
    else:
        command_line_library = CommandLine()
    backup = RoundRobinBackup()
    backup.set_command_line_library(command_line_library)
    backup.backup()
