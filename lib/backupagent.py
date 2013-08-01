class BackupAgent:

    "Base class and shared behavior holder for more specific backup agents."

    def set_options(self, options):
        self.options = options

    def set_command_line_library(self, command_line_library):
        self.cli = command_line_library

    def _execute_command(self, command, *args, **kwargs):
        return self.cli.execute(command, *args, **kwargs)
