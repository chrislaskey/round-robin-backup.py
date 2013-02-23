About
=====

Version 0.8.4

A round-robin backup script using rsync, tar, bzip2, and the
[round-robin-date.py](https://github.com/chrislaskey/round-robin-date.py)
library.

This is a custom "push" style backup library, where the client pushes updates
to the backup server. It is not a good fit for most backup schemes. This is
specific to a backup architecture managed by Puppet where clients are aware
of the server, but the server is not always aware of the clients.

A more traditional "pull" backup system is more versitile, where the server
pulls from the client(s) directly. It is recommended to use one of these, such
as [rsnapshot](http://www.rsnapshot.org/) and
[rdiff](http://rdiff-backup.nongnu.org/) unless there is a compelling use case
for a simple push-based backup system.

This is not a replacement for comprehensive backup systems like
[Bacula](http://www.bacula.org/en/) and [Amanda](http://www.amanda.org/).
Instead this is a backup tool for a specific layer of a comprehensive backup
strategy, automated backups of specific directories, such as the backup of
various live website files.

Documentation
=============

Methods
-------

```RoundRobinBackup().get_options()``` Returns a dictionary of options parsed
from command line arguments.

```RoundRobinBackup().backup()``` Executes a round robin backup in three steps:
1 Syncs files to backup destination using rsync
2 Creates a bzip2 tar archive file on the backup destination 
3 Prunes stale backup archive files on the backup destination based on round-robin-date rules.

Command-line Options
--------------------

The API is still fluid, see ```./roundrobindate.py --help``` for an up-to-date
list of passable command-line options.

License
=======

All code is released under MIT license. See the attached LICENSE.txt file for
more information, including commentary on license choice.
