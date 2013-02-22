#!/usr/bin/env python

import os
from lib.roundrobinbackupoptionsparser import RoundRobinBackupOptionsParser
from lib.roundrobindate import RoundRobinDate
from utilities.commandline import CommandLine
from utilities.sshutilities import SSHCommand

class RoundRobinBackup:

    def __init__(self):
        self._set_options()
        self._set_command_line_library()

    def _set_options(self):
        parser = RoundRobinBackupOptionsParser()
        options = parser.get_options()
        self.options = options

    def get_options(self):
        return self.options.copy()

    def _set_command_line_library(self):
        command_line_library = CommandLine()
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

class AbstractRoundRobinBackupActor:

    def set_options(self, options):
        self.options = options

    def set_command_line_library(self, command_line_library):
        self.cli = command_line_library

    def execute_command(self, command, *args, **kwargs):
        return self.cli.execute(command, *args, **kwargs)

    def execute_pipe(self, commands, *args, **kwargs):
        return self.cli.execute_queue(commands, *args, **kwargs)

class RoundRobinBackupRemoteSync(AbstractRoundRobinBackupActor):

    def sync_files(self):
        self._create_remote_backup_dir_if_needed()
        self._rsync_data()

    def _create_remote_backup_dir_if_needed(self):
        command = self._get_make_backup_dir_command()
        # self.cli.execute(command)

    def _get_make_backup_dir_command(self):
        destination_path = self.options['destination_path']
        rsync_dir = self.options['rsync_dir']
        remote_path = os.path.join(destination_path, rsync_dir)
        remote_command = "/bin/mkdir -p {0}".format(remote_path)
        ssh_command_options = {
            'user': self.options['destination_user'],
            'host': self.options['destination_host'],
            'port': self.options['ssh_port'],
            'identity_file': self.options['ssh_identity_file'],
            'subcommand': remote_command
        }
        ssh_command = SSHCommand().create(ssh_command_options)
        return ssh_command

    def _rsync_data(self):
        rsync_command = self._get_backup_rsync_command()
        # self.cli.execute(rsync_command)

    def _get_backup_rsync_command(self):
        rsync = ['rsync']
        flags = ['-avz']
        ssh_commands = self._get_ssh_command()
        source = [self.options['source']]
        target = self._get_rsync_target()
        excludes = self._get_exclude_commands()
        command = rsync + flags + ssh_commands + source + target + excludes
        return command

    def _get_ssh_command(self):
        options = {
            'port': self.options['ssh_port'],
            'identity_file': self.options['ssh_identity_file'],
        }
        ssh_command = SSHCommand().create_command_string(options)
        rsync_command = []
        rsync_command.append('-e')
        rsync_command.append('{0}'.format(ssh_command))
        return rsync_command

    def _get_rsync_target(self):
        destination = self.options['destination']
        rsync_dir = self.options['rsync_dir']
        rsync_destination = [os.path.join(destination, rsync_dir)]
        return rsync_destination

    def _get_exclude_commands(self):
        excludes_command = []
        for item in self.options['exclude']:
            excludes_command.append('--exclude')
            excludes_command.append(item)
        return excludes_command

class RoundRobinBackupRemoteArchive(AbstractRoundRobinBackupActor):

    # Create today's archive dir
    # Use live backup dir to tar+bzip2 files
    # tar -cjf rrbackup-<date>.tar.bzip2 latest
    # Create backup readme file.
    pass

class RoundRobinBackupRemoteCleanup(AbstractRoundRobinBackupActor):
    
    def cleanup_backups(self):
        self._set_existing_backups()
        self._remove_stale_backups()

    def _set_existing_backups(self):
        existing_backups = self._get_list_of_existing_backups()
        self.existing_backups = existing_backups

    def _get_list_of_existing_backups(self):
        list_of_files = self._get_remote_backup_dir_files_list()
        backup_prefix = self.options['backup_prefix']
        backup_files = [name for name in list_of_files if backup_prefix in name]
        backup_objects = []
        for filename in backup_files:
            backup_object = self._create_backup_file_object(filename)
            backup_objects.append(backup_object)
        return backup_objects

    def _get_remote_backup_dir_files_list(self):
        command = self._get_remote_list_command()
        # result = self.cli.execute(command)
        files_as_list = result.split('\n')
        filtered_list = [x for x in files_as_list if x]
        return filtered_list
        
    def _get_remote_list_command(self):
        remote_path = self.options['destination_path']
        ls_subcommand = 'ls {0}'.format(remote_path)
        ssh_command_options = {
            'user': self.options['destination_user'],
            'host': self.options['destination_host'],
            'port': self.options['ssh_port'],
            'identity_file': self.options['ssh_identity_file'],
            'subcommand': ls_subcommand
        }
        ssh_command = SSHCommand().create(ssh_command_options)
        return ssh_command

    def _create_backup_file_object(self, filename):
        date = self._get_date_from_backup_filename(filename)
        backup_object = {}
        backup_object['filename'] = filename
        backup_object['date'] = date
        return backup_object

    def _get_date_from_backup_filename(self, filename):
        '''
        Parse date from backup filename like
        automated-backup-2012-02-01.tar.bzip2
        '''
        backup_prefix = self.options['backup_prefix']
        prefix_length = len(backup_prefix)
        if '.' in filename:
            first_period = filename.index('.')
            filename_less_extension = filename[:first_period]
        else:
            filename_less_extension = filename
        date = filename_less_extension[prefix_length:]
        return date

    def _remove_stale_backups(self):
        files_to_remove = self._get_files_to_remove()
        # print(files_to_remove)
        # TODO
        # remove_files_command = self._get_remove_files_command(files_to_remove)
        # self.cli.execute(remove_files_command)

    def _get_files_to_remove(self):
        dates_to_keep = self._get_backup_dates_to_keep()
        files_to_remove = []
        for backup in self.existing_backups:
            date = backup.get('date')
            if date not in dates_to_keep:
                filename = backup.get('filename')
                files_to_remove.append(filename)
        return files_to_remove

    def _get_backup_dates_to_keep(self):
        date_library = self._create_date_library()
        dates = date_library.get_dates_as_strings()
        return dates

    def _create_date_library(self):
        # TODO: self.oldest_backup_date
        options = {
            'days_to_retain': self.options['days'],
            'weeks_to_retain': self.options['weeks'],
            'months_to_retain': self.options['months'],
            'years_to_retain': self.options['years'],
            # 'anchor_date': self.oldest_backup_date
        }
        date_library = RoundRobinDate(options)
        return date_library

if __name__ == "__main__":
    RoundRobinBackup().backup()
