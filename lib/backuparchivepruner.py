import os
from lib.backupagent import BackupAgent
from utilities.roundrobindate import RoundRobinDate
from utilities.sshutilities import SSHCommand


class BackupArchivePruner(BackupAgent):
    
    def cleanup_backups(self):
        self._set_existing_backups()
        self._remove_stale_backups()

    def _set_existing_backups(self):
        existing_backups = self._get_list_of_existing_backups()
        self.existing_backups = existing_backups

    def _get_list_of_existing_backups(self):
        list_of_files = self._get_remote_backup_dir_files_list()
        backup_prefix = self.options['backup_prefix']
        backup_filenames = [name for name in list_of_files if backup_prefix in name]
        backup_files = []
        for filename in backup_filenames:
            backup_file = self._create_backup_file_dictionary(filename)
            backup_files.append(backup_file)
        return backup_files

    def _get_remote_backup_dir_files_list(self):
        command = self._get_remote_list_command()
        command_results = self._execute_command(command)
        remote_files = self._parse_files_from_results(command_results)
        return remote_files
        
    def _get_remote_list_command(self):
        remote_path = self.options['destination_path']
        ls_subcommand = '/bin/ls {0}'.format(remote_path)
        ssh_command_options = {
            'user': self.options['destination_user'],
            'host': self.options['destination_host'],
            'port': self.options['ssh_port'],
            'identity_file': self.options['ssh_identity_file'],
            'subcommand': ls_subcommand
        }
        ssh_command = SSHCommand().create(ssh_command_options)
        return ssh_command

    def _parse_files_from_results(self, remote_command_results):
        files = []
        if remote_command_results:
            files_as_list = remote_command_results.split('\n')
            files = [x for x in files_as_list if x]
        return files

    def _create_backup_file_dictionary(self, filename):
        date = self._get_date_from_backup_filename(filename)
        path = self.options['destination_path']
        backup_dict = {}
        backup_dict['filename'] = filename
        backup_dict['fullpath'] = os.path.join(path, filename)
        backup_dict['date'] = date
        return backup_dict

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
        remove_files_command = self._get_remove_files_command()
        if remove_files_command:
            self._execute_command(remove_files_command)

    def _get_remove_files_command(self):
        subcommand = self._get_remove_files_subcommand()
        if not subcommand:
            return ''
        ssh_command_options = {
            'user': self.options['destination_user'],
            'host': self.options['destination_host'],
            'port': self.options['ssh_port'],
            'identity_file': self.options['ssh_identity_file'],
            'subcommand': subcommand
        }
        ssh_command = SSHCommand().create(ssh_command_options)
        return ssh_command
        
    def _get_remove_files_subcommand(self):
        files = self._get_files_to_remove()
        if not files:
            return ''
        files_to_remove = ' '.join(files)
        rm_command = '/bin/rm -r {0}'.format(files_to_remove)
        return rm_command

    def _get_files_to_remove(self):
        dates_to_keep = self._get_backup_dates_to_keep()
        files_to_remove = []
        for backup in self.existing_backups:
            date = backup.get('date')
            if date not in dates_to_keep:
                fullpath = backup.get('fullpath')
                files_to_remove.append(fullpath)
        return files_to_remove

    def _get_backup_dates_to_keep(self):
        date_library = self._create_date_library()
        dates = date_library.get_dates_as_strings()
        if self.oldest_backup_date:
            dates.append(self.oldest_backup_date)
        return dates

    def _create_date_library(self):
        self._set_oldest_backup_date()
        options = {
            'days_to_retain': self.options['days'],
            'weeks_to_retain': self.options['weeks'],
            'months_to_retain': self.options['months'],
            'years_to_retain': self.options['years'],
            'anchor_date': self.oldest_backup_date
        }
        date_library = RoundRobinDate(options)
        return date_library

    def _set_oldest_backup_date(self):
        existing_backups = self.existing_backups
        if existing_backups:
            dates = [backup['date'] for backup in existing_backups]
            dates.sort()
            oldest_backup_date = dates[0]
        else:
            oldest_backup_date = ''
        self.oldest_backup_date = oldest_backup_date
