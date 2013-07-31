class CommandLineStub:

    def execute(self, command, **extra_params_not_used_in_testing):
        command_as_string = ' '.join(command)
        return (command_as_string, command)

    def execute_queue(self, commands, return_boolean=False):
        return commands


class CommandLineStubPrinter:
    ' Used with --debug flag to noop and print commands'
    def execute(self, command, **extra_params_not_used_in_testing):
        command_as_string = ' '.join(command)
        print('\n# Debug flag set, in noop mode. Would have executed command:')
        print(command_as_string)
        print(command)

    def execute_queue(self, commands, return_boolean=False):
        print('Executing command:')
        print(commands)


class CommandLineMock:

    def __init__(self, list_of_tuples_of_command_and_return_value):
        self.expected_commands = list_of_tuples_of_command_and_return_value

    def execute(self, command, *extra_params_not_used_in_testing):
        command_as_string = ' '.join(command)
        output = self._get_output(command_as_string)
        return output

    def _get_output(self, given_command):
        expected_command, expected_result = self.expected_commands.pop(0)
        if given_command != expected_command:
            raise Exception('Given command not found in CommandLine testing '
                            'mock "{0}". Expected: "{1}"'
                            .format(given_command, expected_command))
        return expected_result

    def execute_queue(self, commands, **extra_params_not_used_in_testing):
        flattened = [item for sublist in list for item in sublist]
        command_as_string = ' '.join(flattened)
        output = self._get_output(command_as_string)
        return output
