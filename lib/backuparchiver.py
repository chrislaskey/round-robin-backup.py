from lib.backupagent import BackupAgent

class BackupArchiver(BackupAgent):

    # Create today's archive dir
    # Use live backup dir to tar+bzip2 files
    # tar -cjf rrbackup-<date>.tar.bzip2 latest
    # Create backup readme file.

    def create(self):
        pass

