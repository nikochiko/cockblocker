import signal
import subprocess
import sys


PYTHON_EXEC = "python3"


def get_args():
    script, args = sys.argv[1], sys.argv[2:]
    return script, args


def monitor(script, args):
    print("starting process:", PYTHON_EXEC, script, *args)
    proc = subprocess.Popen([PYTHON_EXEC, script, *args],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    print("process started. pid:", proc.pid)
    return_code = proc.wait()
    print(f"process exited with return code: {return_code}")


def log_signal_and_ignore(sig, frame):
    signame = signal.Signals(sig).name
    print(f"ignoring signal {signame}")


if __name__ == "__main__":
    signal.signal(signal.SIGHUP, log_signal_and_ignore)
    signal.signal(signal.SIGINT, log_signal_and_ignore)

    script, args = get_args()

    while True:
        monitor(script, args)
