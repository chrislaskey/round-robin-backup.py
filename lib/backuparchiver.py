import os
from lib.backupagent import BackupAgent
from utilities.roundrobindate import RoundRobinDate
from utilities.sshutilities import SSHCommand


class BackupArchiver(BackupAgent):

    def execute(self):
        'Create an archival tar on the remote target'
        ssh_command = self._get_ssh_command()
        self._execute_command(ssh_command)

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
        backup_path = self.options['destination_path']
        backup_fullpath = self._get_backup_fullpath()
        rsync_dir = self.options['rsync_dir']
        tar_command = '/bin/tar -C {0} -cjf {1} {2}'.format(
            backup_path, backup_fullpath, rsync_dir
        )
        return tar_command

    def _get_backup_fullpath(self):
        date = RoundRobinDate()
        backup_path = self.options['destination_path']
        backup_prefix = self.options['backup_prefix']
        backup_date = date.get_today()
        backup_filename = '{0}{1}.tar.bzip2'.format(backup_prefix, backup_date)
        backup_fullpath = os.path.join(backup_path, backup_filename)
        return backup_fullpath
