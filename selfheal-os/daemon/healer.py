import os
import subprocess
import logging

from .config import load_config

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'events.log')
logging.basicConfig(filename=LOG_PATH, level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

class Healer:
    def __init__(self):
        self.config = load_config()

    def restart_service(self, service):
        logging.info('Restarting service %s', service)
        subprocess.run(['systemctl', 'restart', service], check=False)

    def kill_process(self, pid):
        logging.info('Killing process %s', pid)
        subprocess.run(['kill', '-9', str(pid)], check=False)
