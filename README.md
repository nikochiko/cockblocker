# cockblocker

cockblocker (named after a scene in the Seth Rogen movie Superbad) is a Python script that
that will block certain websites (configurable) by setting them to some other IP in
`/etc/hosts`. If a change to one of the block listed hosts is detected by cockblocker (it polls),
it will once again set that back to the blocking IP.

It would be too easy if that were it, anyone would be able to just stop the process and make their edits.
cockblocker comes with a monitor script for itself that will keep re-spawning this process when it dies.
This monitor script won't respond to `SIGINT` (Ctrl+C interrupt) or `SIGHUP` (`kill`). It can only be
killed with `SIGKILL` and even then it won't stop the blocker script. The blocker script will keep running
and has to be stopped. One could, if they so dared, build a chain of such process (monitor the monitoring
process and so on) to keep making it harder to stop the blocking.

For the normal human, it should be enough to start a process with one or two recursive monitors.
You can also set this up as a startup process with systemd or init or cron.

### Usage

To edit the hosts list, there isn't a configuration file (that would be too easy, wouldn't it?). The list
is a Python list hardcoded in `blocker.py` as a global variable.

To start the script, you can run the `start.sh` script. By default this will start one monitor for one
blocker process. You can edit the `start.sh` script easily to add more.

```shell
# start.sh

python3 monitor_process.py blocker.py /etc/hosts

# to create a chain of more monitoring process, just repeat monitor_process.py that many times. For example

python3 monitor_process.py monitor_process.py monitor_process.py blocker.py /etc/hosts

# this will create a chain of 3 monitoring process and one blocker process.
```
