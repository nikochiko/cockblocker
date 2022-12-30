# cockblocker

cockblocker (named after a scene in the movie Superbad) is a Python script that
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

Run the `start.sh` script to start the blocker.
```shell
$ start.sh
Password: 
# starts ...
```

The blocked hosts list isn't stored in a configuration file (that would be too easy, wouldn't it?). Instead,
the list is a Python list hardcoded in `blocker.py` as a global variable. You will need to edit that to
add or remove websites from the blocking list.

You can build a chain of monitors too to make it even harder for yourself to stop this blocker script. To
do that, you can easily edit the `start.sh` script to do that.

```shell
# start.sh
python3 monitor_process.py blocker.py /etc/hosts

# to create a chain of more monitoring process, just repeat monitor_process.py that many times. For example
python3 monitor_process.py monitor_process.py monitor_process.py blocker.py /etc/hosts
# this will create a chain of 3 monitoring process and one blocker process.
# Technology of our time (copy-paste) makes it very easy to do this multiple times.
# In vim, you can select it and paste it 100s of times with a few keystrokes.
```

### How it works

We use Python subprocess to start a new process from `monitor_process.py`. We wait for it to finish (the blocker
process shouldn't finish because it should run in an infinite loop) and when it does we respawn it. We ignore
SIGINT and SIGHUP by setting handlers using the [`signal`](https://docs.python.org/3/library/signal.html) module.
We also don't try to kill the child processes when our main process dies. So if you try to be clever and kill the monitor
process, you will still have to kill the blocker separately. To make a neat clean, you will have to follow a top-down order
and kill all the monitor processes before coming to the blocker.

The monitor script is generic and works for other Python scripts too. Its first argument is the
path to the python script to run, and the rest are args that are passed to this script. This makes it possible to chain
monitor processes very easily (with copy-paste), with the parent of each process making sure the child is alive and so on.
Note that killing a process in the middle of a chain will actually start another instance of the rest of the chain. In that case you
will end up with two instances of the base process (in our case, the blocker). I won't so much as call it a bug because
it makes it even harder to stop the blocker process. Hugely Monstrous.

Please note that I haven't thought of how the process should be killed cleanly (read that again). Easiest way is to
restart your computer. If you only have a chain of one or two monitors, you can `ps a | grep monitor_process.py` and
`ps a | grep blocker.py` and make a `sudo kill -9 <pid>` with the PID. It could be possible to write a script that
kills the processes one by one, but that should make sure that the killing is done in the correct order or you'll
end up with even more processes than before. There could be other ways of combatting this such as creating your own
fighting script that keeps removing the blocked websites from `/etc/hosts`.

I wonder if it's possilbe to build a circular structure of processes that keep respawning each other.

### LICENSE

Licensed under MIT License.
