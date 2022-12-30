import sys
import time


REDIRECTION_IP = "127.0.0.1"
POLL_INTERVAL = 5  # seconds

BLOCK_LIST = [
    "discord.com",
    "discordapp.com",
    "instagram.com",
    "twitter.com",
    "api.twitter.com",
]


def block(hosts_file, block_list):
    with open(hosts_file, "r+") as f:
        hosts = get_hosts(f.read())
        print("hosts: ")

        to_add = {}
        for host in block_list:
            if host not in hosts or hosts[host] != REDIRECTION_IP:
                to_add[host] = REDIRECTION_IP

        print("adding hosts: ", to_add)
        write_hosts(f, to_add)


def get_hosts(hosts_content):
    result = {}
    for line in hosts_content.splitlines():
        comment_start = line.find("#")
        if comment_start != -1:
            line = line[:comment_start]

        parts = line.strip().split()
        if not len(parts) >= 2:
            continue
        else:
            ip, host = parts[:2]
            result[host] = ip

    return result


def write_hosts(fd, hosts):
    for host, ip in hosts.items():
        fd.write(format_host(host, ip))


def format_host(host, ip):
    return f"{ip}\t{host}\t# added by cockblocker\n"


def get_args(argv):
    if len(argv) != 2:
        print("Need path to hosts file as the first argument")
        sys.exit(1)

    return sys.argv[1:]


if __name__ == "__main__":
    hosts_file, = get_args(sys.argv)

    print("starting the blocker")
    while True:
        block(hosts_file, BLOCK_LIST)
        time.sleep(POLL_INTERVAL)
