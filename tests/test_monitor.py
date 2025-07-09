import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'selfheal-os'))
from daemon.monitor import Monitor


def test_check_threshold(monkeypatch):
    mon = Monitor()
    monkeypatch.setattr(mon, 'system_usage', lambda: {'cpu': 95, 'ram': 40, 'disk': 40})
    alerts = mon.check_thresholds()
    assert any('High CPU' in a for a in alerts)
