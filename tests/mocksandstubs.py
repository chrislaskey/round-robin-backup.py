class CommandLineStub:

    def execute(self, command, stdin=None, stdout=None, stderr=None,
                return_boolean=False):
        print(command)
        return ''

    def execute_queue(self, commands, return_boolean=False):
        print(commands)
        return ''

