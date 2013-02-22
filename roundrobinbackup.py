#!/usr/bin/env python

from lib.roundrobinbackupoptionsparser import RoundRobinBackupOptionsParser
from lib.roundrobinbackupremotesync import RoundRobinBackupRemoteSync
from lib.roundrobinbackupremotearchive import RoundRobinBackupRemoteArchive
from lib.roundrobinbackupremotecleanup import RoundRobinBackupRemoteCleanup
from utilities.commandline import CommandLine

class RoundRobinBackup:

    def __init__(self):
        self._set_options()

    def _set_options(self):
        parser = RoundRobinBackupOptionsParser()
        options = parser.get_options()
        self.options = options

    def get_options(self):
        return self.options.copy()

    def set_command_line_library(self, command_line_library):
        self.command_line_library = command_line_library

    def backup(self):
        self._remote_sync()
        # TODO: implement
        # self._remote_archive()
        # self._remote_cleanup()

    def _remote_sync(self):
        sync = self._create_remote_actor('sync')
        sync.sync_files()

    def _create_remote_actor(self, type):
        remote = self._remote_actor_simple_factory(type)
        remote.set_options(self.options)
        remote.set_command_line_library(self.command_line_library)
        return remote

    def _remote_actor_simple_factory(self, type):
        if type == 'sync':
            remote = RoundRobinBackupRemoteSync()
        elif type == 'archive':
            remote = RoundRobinBackupRemoteArchive()
        elif type == 'cleanup':
            remote = RoundRobinBackupRemoteCleanup()
        return remote

    def _remote_archive(self):
        archive = self._create_remote_actor('archive')
        archive.create_archive()

    def _remote_cleanup(self):
        cleanup = self._create_remote_actor('cleanup')
        cleanup.cleanup_backups()

if __name__ == "__main__":
    command_line_library = CommandLine()
    backup = RoundRobinBackup()
    backup.set_command_line_library(command_line_library)
    backup.backup()
