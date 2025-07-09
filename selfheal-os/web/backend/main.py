from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from daemon.monitor import Monitor
from daemon.healer import Healer

app = FastAPI()
mon = Monitor()
healer = Healer()
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs', 'events.log')


class Action(BaseModel):
    action: str


@app.get('/status')
def status():
    return {
        'usage': mon.system_usage(),
        'services': mon.list_services()
    }


@app.get('/log')
def log():
    with open(LOG_PATH) as f:
        lines = f.readlines()[-50:]
    return {'log': lines}


@app.post('/action/{service}')
def control_service(service: str, data: Action):
    if data.action == 'restart':
        healer.restart_service(service)
    elif data.action == 'kill':
        # service expected to be pid for kill
        healer.kill_process(service)
    else:
        raise HTTPException(400, 'Unknown action')
    return {'status': 'ok'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=23673)
