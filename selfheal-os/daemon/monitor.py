import os
import psutil
import subprocess
import time
import logging
from .config import load_config

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'events.log')
logging.basicConfig(filename=LOG_PATH, level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

class Monitor:
    def __init__(self):
        self.config = load_config()
        self.exclude = set(self.config.get('exclude_services', []))

    def system_usage(self):
        return {
            'cpu': psutil.cpu_percent(interval=1),
            'ram': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('/').percent
        }

    def list_services(self):
        result = subprocess.run(['systemctl', 'list-units', '--type=service', '--state=running', '--no-pager', '--no-legend'],
                                stdout=subprocess.PIPE, text=True, check=False)
        services = []
        for line in result.stdout.splitlines():
            if not line:
                continue
            svc = line.split()[0]
            if svc not in self.exclude:
                services.append(svc)
        return services

    def log_status(self):
        usage = self.system_usage()
        logging.info('System usage: CPU %(cpu)s%% RAM %(ram)s%% DISK %(disk)s%%', usage)
        for svc in self.list_services():
            logging.info('Service running: %s', svc)

    def check_thresholds(self):
        usage = self.system_usage()
        alerts = []
        if usage['cpu'] > self.config.get('cpu_threshold', 90):
            alerts.append('High CPU: %.2f%%' % usage['cpu'])
        if usage['ram'] > self.config.get('ram_threshold', 85):
            alerts.append('High RAM: %.2f%%' % usage['ram'])
        if usage['disk'] > self.config.get('disk_threshold', 90):
            alerts.append('High DISK: %.2f%%' % usage['disk'])
        return alerts

    def run(self, interval=60):
        while True:
            self.log_status()
            alerts = self.check_thresholds()
            for alert in alerts:
                logging.warning(alert)
            time.sleep(interval)
