"""Simple log analyzer that suggests config changes."""
import os
import logging
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_PATH = os.path.join(BASE_DIR, 'logs', 'events.log')
LEARNED_LOG_PATH = os.path.join(BASE_DIR, 'logs', 'learned_actions.log')
logging.basicConfig(filename=LOG_PATH, level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')


class Learner:
    def __init__(self, threshold: int = 3):
        self.threshold = threshold

    def analyze_logs(self):
        if not os.path.exists(LOG_PATH):
            return {}
        counts = Counter()
        with open(LOG_PATH) as f:
            for line in f:
                if 'Restarting service' in line:
                    svc = line.split('Restarting service')[-1].strip()
                    counts[svc] += 1
                elif 'Killing process' in line:
                    proc = line.split('Killing process')[-1].strip()
                    counts[proc] += 1
        recommendations = {}
        for item, cnt in counts.items():
            if cnt >= self.threshold:
                msg = f'Recommend investigation of {item} (occurred {cnt} times)'
                recommendations[item] = msg
        if recommendations:
            with open(LEARNED_LOG_PATH, 'a') as f:
                for item, msg in recommendations.items():
                    f.write(f'{item}: {msg}\n')
        return recommendations