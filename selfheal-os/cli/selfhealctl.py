#!/usr/bin/env python3
import argparse
import psutil
import subprocess
import logging
import os

from daemon.monitor import Monitor
from daemon.healer import Healer

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'events.log')


def show_status():
    mon = Monitor()
    usage = mon.system_usage()
    services = mon.list_services()
    print('CPU: {cpu}% RAM: {ram}% DISK: {disk}%'.format(**usage))
    print('Services:')
    for s in services:
        print(' -', s)


def show_log(lines=10):
    with open(LOG_PATH, 'r') as f:
        for line in f.readlines()[-lines:]:
            print(line.rstrip())


def restart(service):
    healer = Healer()
    healer.restart_service(service)


def kill(pid):
    healer = Healer()
    healer.kill_process(pid)


def main():
    parser = argparse.ArgumentParser(description='Self-healing OS CLI')
    sub = parser.add_subparsers(dest='command')

    sub.add_parser('status')
    sub.add_parser('log').add_argument('-n', type=int, default=10)

    r = sub.add_parser('restart')
    r.add_argument('service')

    k = sub.add_parser('kill')
    k.add_argument('pid', type=int)

    args = parser.parse_args()
    if args.command == 'status':
        show_status()
    elif args.command == 'log':
        show_log(args.n)
    elif args.command == 'restart':
        restart(args.service)
    elif args.command == 'kill':
        kill(args.pid)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
