import os
from lib.backupagent import BackupAgent
from utilities.sshutilities import SSHCommand

class BackupCreator(BackupAgent):

    def sync_files(self):
        self._create_remote_backup_dir_if_needed()
        self._rsync_data()

    def _create_remote_backup_dir_if_needed(self):
        command = self._get_make_backup_dir_command()
        self.cli.execute(command)

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
        self.cli.execute(rsync_command)

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
