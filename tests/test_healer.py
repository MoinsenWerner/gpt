import os
import sys
import subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'selfheal-os'))
from daemon.healer import Healer


def test_restart_service(monkeypatch):
    calls = []
    def fake_run(cmd, check=False):
        calls.append(cmd)
    monkeypatch.setattr(subprocess, 'run', fake_run)
    h = Healer()
    h.restart_service('dummy.service')
    assert calls[0][:2] == ['systemctl', 'restart']
