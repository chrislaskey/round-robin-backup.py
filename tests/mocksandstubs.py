class CommandLineStub:

    def execute(self, command, stdin=None, stdout=None, stderr=None,
                return_boolean=False):
        print(command)
        return ''

    def execute_queue(self, commands, return_boolean=False):
        print(commands)
        return ''

class CommandLineMock:

    def __init__(self, input_output, order_matters = True):
        self.order_matters = order_matters
        self.input_output = input_output

    def _get_output(self, command_as_string):
        if self.order_matters:
            input_output = self.input_output.pop(0)
            input = input_output[0]
            output = input_output[1]
            if command_as_string != input:
                raise Exception('Command not found in CommandLine testing '
                                'mock "{0}"'.format(command_as_string))
            return output
        else:
            for tup in self.input_output:
                if tup[0] == command_as_string:
                    return tup[1]
            raise Exception('Command not found in CommandLine testing '
                            'mock "{0}"'.format(command_as_string))

    def execute(self, command, stdin=None, stdout=None, stderr=None,
                return_boolean=False):
        command_as_string = ' '.join(command)
        output = self._get_output(command_as_string)
        return output

    def execute_queue(self, commands, return_boolean=False):
        flattened = [item for sublist in list for item in sublist]
        command_as_string = ' '.join(flattened)
        output = self._get_output(command_as_string)
        return output
