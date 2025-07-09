import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'selfheal-os'))
from fastapi.testclient import TestClient
from web.backend.main import app, mon, healer


def test_status_endpoint(monkeypatch):
    monkeypatch.setattr(mon, 'system_usage', lambda: {'cpu': 10, 'ram': 10, 'disk': 10})
    monkeypatch.setattr(mon, 'list_services', lambda: ['a.service'])
    client = TestClient(app)
    resp = client.get('/status', headers={'Authorization': 'Bearer changeme'})
    assert resp.status_code == 200
    data = resp.json()
    assert data['usage']['cpu'] == 10
    assert 'a.service' in data['services']


def test_action_restart(monkeypatch):
    called = {}
    def fake_restart(svc):
        called['svc'] = svc
    monkeypatch.setattr(healer, 'restart_service', fake_restart)
    client = TestClient(app)
    resp = client.post('/action/test.service', json={'action':'restart'},
                       headers={'Authorization': 'Bearer changeme'})
    assert resp.status_code == 200
    assert called['svc'] == 'test.service'
