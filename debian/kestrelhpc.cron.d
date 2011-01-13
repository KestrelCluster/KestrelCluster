#
# Regular cron jobs for the test package
#

*/1 * * * *	root	[ -x /usr/sbin/kestrel-cron ] && /usr/sbin/kestrel-cron --check
