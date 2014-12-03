#!/bin/sh

### BEGIN INIT INFO
# Provides: uwsgi
# Required-Start: $all
# Required-Stop: $all
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: starts the uwsgi {{ uwsgi.app_name }} server
# Description: starts uwsgi {{ uwsgi.app_name }} server using start-stop-daemon
### END INIT INFO

PATH=/opt/uwsgi:/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/bin

# Activate pyenv and virtualenv
export PYENV_ROOT={{ pyenv.root }}
export PATH=$PYENV_ROOT/bin:$PATH;
pyenv local {{ pyenv.version }}
eval "$(pyenv init -)"
pyenv activate {{ pyenv.virtualenv_name }}

DAEMON="{{ uwsgi.virtualenv }}/bin/uwsgi"
OWNER="{{ uwsgi.user }}"
GROUP="{{ uwsgi.group }}"
NAME="{{ uwsgi.app_name }}"
DESC="{{ uwsgi.app_name }}"

test -x $DAEMON || exit 0

set -e

DAEMON_OPTS="--ini {{ uwsgi.ini_file }}"

case "$1" in
    start)
        echo -n "Starting $DESC: "
        start-stop-daemon --start --chuid $OWNER:$GROUP --user $OWNER --exec $DAEMON -- $DAEMON_OPTS
        echo "$NAME."
        ;;
    stop)
        echo -n "Stopping $DESC: "
        start-stop-daemon --signal 3 --user $OWNER --quiet --retry 2 --stop --exec $DAEMON
        echo "$NAME."
        ;;
    reload)
        killall -1 $DAEMON
        ;;
    force-reload)
        killall -15 $DAEMON
        ;;
    restart)
        echo -n "Restarting $DESC: "
        start-stop-daemon --signal 3 --user $OWNER --quiet --retry 2 --stop --exec $DAEMON
        sleep 1
        start-stop-daemon --user $OWNER --start --quiet --chuid $OWNER:$GROUP --exec $DAEMON -- $DAEMON_OPTS
        echo "$NAME."
        ;;
    status)
        killall -10 $DAEMON
        ;;
    *)
        N=/etc/init.d/$NAME
        echo "Usage: $N {start|stop|restart|reload|force-reload|status}" >&2
        exit 1
        ;;
esac
exit 0
