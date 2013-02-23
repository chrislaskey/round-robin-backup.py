import os
from lib.backupagent import BackupAgent
from utilities.roundrobindate import RoundRobinDate
from utilities.sshutilities import SSHCommand

class BackupArchiver(BackupAgent):

    def create(self):
        ssh_command = self._get_ssh_command()
        self.cli.execute(ssh_command)

    def _get_ssh_command(self):
        subcommand = self._get_tar_subcommand()
        ssh_command_options = {
            'user': self.options['destination_user'],
            'host': self.options['destination_host'],
            'port': self.options['ssh_port'],
            'identity_file': self.options['ssh_identity_file'],
            'subcommand': subcommand
        }
        ssh_command = SSHCommand().create(ssh_command_options)
        return ssh_command

    def _get_tar_subcommand(self):
        backup_fullpath = self._get_backup_fullpath()
        rsync_fullpath = self._get_rsync_fullpath()
        tar_command = '/bin/tar -cjf {0} {1}'.format(
            backup_fullpath, rsync_fullpath
        )
        return tar_command

    def _get_backup_fullpath(self):
        date = RoundRobinDate()
        path = self.options['destination_path']
        backup_prefix = self.options['backup_prefix']
        backup_date = date.get_today()
        backup_filename = '{0}{1}.tar.bzip2'.format(backup_prefix, backup_date)
        backup_fullpath = os.path.join(path, backup_filename)
        return backup_fullpath

    def _get_rsync_fullpath(self):
        path = self.options['destination_path']
        rsync_dir = self.options['rsync_dir']
        rsync_fullpath = os.path.join(path, rsync_dir)
        return rsync_fullpath
