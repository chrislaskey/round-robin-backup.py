About
================================================================================

A round-robin backup script using rsync, tar, bzip2, and the round-robin-date.py
library.

This is a custom "push" style backup library, where the client pushes updates
to the backup server. It is not a good fit for most backup schemes. This is
specific to a backup architecture managed by Puppet where clients are aware
of the server, but the server is not always aware of the clients.

A more traditional "pull" backup system is more versitile, where the server
pulls from the client(s) directly. It is recommended to use one of these,
such as **rsnapshot** and **rdiff** unless there is a compelling use case
for a simple push-based backup system.

This is not a replacement for comprehensive backup systems like **Bacula** or
**Amanda**.

License
================================================================================

All code is released under MIT license. See the attached LICENSE.txt file for
more information, including commentary on license choice.
