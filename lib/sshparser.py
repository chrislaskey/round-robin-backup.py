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
