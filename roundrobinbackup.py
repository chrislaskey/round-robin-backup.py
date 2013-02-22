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
        # self._create_archive()
        # self._remove_stale_archives()

    def _create_backup(self):
        creator = self._create_remote_actor('creator')
        creator.sync_files()

    def _create_remote_actor(self, type):
        remote = self._remote_actor_simple_factory(type)
        remote.set_options(self.options)
        remote.set_command_line_library(self.command_line_library)
        return remote

    def _remote_actor_simple_factory(self, type):
        if type == 'creator':
            remote = BackupCreator()
        elif type == 'archiver':
            remote = BackupArchiver()
        elif type == 'archive_pruner':
            remote = BackupArchivePruner()
        return remote

    def _create_archive(self):
        archiver = self._create_remote_actor('archiver')
        archiver.create()

    def _remove_stale_archives(self):
        archive_pruner = self._create_remote_actor('archive_pruner')
        archive_pruner.cleanup_backups()

if __name__ == "__main__":
    command_line_library = CommandLine()
    backup = RoundRobinBackup()
    backup.set_command_line_library(command_line_library)
    backup.backup()
