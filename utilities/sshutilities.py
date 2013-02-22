class SSHCommand:

    def create(self, options):
        self._parse_options(options)
        command = self._get_command()
        return command
    
    def create_command_string(self, options):
        command_list = self.create(options)
        command_string = ' '.join(command_list)
        return command_string

    def _parse_options(self, options):
        self.user = options.get('user', '')
        self.host = options.get('host', '')
        self.port = options.get('port', '')
        self.identity_file = options.get('identity_file', '')
        self.subcommand = options.get('subcommand', '')

    def _get_command(self):
        args = self._get_args()
        command_pieces = ['ssh'] + args['target'] + args['port'] + \
                         args['identity_file'] + args['subcommand']
        filtered_command_pieces = [x for x in command_pieces if x]
        return filtered_command_pieces

    def _get_args(self):
        args = {
            'target': self._create_target_arg(),
            'port': self._create_port_arg(),
            'identity_file': self._create_identity_file_arg(),
            'subcommand': self._create_subcommand()
        }
        return args

    def _create_target_arg(self):
        target = []
        if self.user:
            target.append('{0}@{1}'.format(self.user, self.host))
        elif self.host:
            target.append(self.host)
        return target

    def _create_port_arg(self):
        port = []
        if self.port and self.port != '22':
            port.append('-p')
            port.append('{0}'.format(self.port))
        return port

    def _create_identity_file_arg(self):
        identity = []
        if self.identity_file:
            identity.append('-i')
            identity.append('{0}'.format(self.identity_file))
        return identity

    def _create_subcommand(self):
        """
        Due to the way Python subprocess executes commands, subcommands like
        'ssh user@host "ls -la"' should not have the wrapping quote marks.
        """
        subcommand = []
        if self.subcommand:
            without_wrapping_quotes = self.subcommand.replace('"', '')
            without_wrapping_quotes = without_wrapping_quotes.replace("'", '')
            subcommand.append(without_wrapping_quotes)
        return subcommand

class SSHParser:

    def parse(self, ssh_string):
        self._parse_pieces(ssh_string)
        pieces = {
            'user': self.user,
            'host': self.host,
            'path': self.path
        }
        return pieces

    def _parse_pieces(self, ssh_string):
        '''
        Assumes a 'user@host:/path' string with pieces possibly omitted.
        Starts from rightmost and moves left.
        '''
        if ':' not in ssh_string:
            self.user = ''
            self.host = ''
            self.path = ssh_string
            return

        colin_position = ssh_string.index(':')

        if '@' not in ssh_string:
            self.user = ''
            self.host = ssh_string[:colin_position]
            self.path = ssh_string[colin_position+1:]
            return

        at_position = ssh_string.index('@')

        self.user = ssh_string[:at_position]
        self.host = ssh_string[at_position+1:colin_position]
        self.path = ssh_string[colin_position+1:]
