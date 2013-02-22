from lib.abstractroundrobinbackupremoteactor import AbstractRoundRobinBackupRemoteActor
from lib.roundrobindate import RoundRobinDate
from utilities.sshutilities import SSHCommand

class RoundRobinBackupRemoteCleanup(AbstractRoundRobinBackupRemoteActor):
    
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

