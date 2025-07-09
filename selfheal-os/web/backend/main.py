from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from daemon.monitor import Monitor
from daemon.healer import Healer

app = FastAPI()
mon = Monitor()
healer = Healer()
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs', 'events.log')

load_dotenv()
API_KEY = os.getenv('API_KEY')


def verify_key(authorization: str = Header(default=None)):
    if API_KEY and authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail='Unauthorized')


class Action(BaseModel):
    action: str


@app.get('/status')
def status(dep=Depends(verify_key)):
    return {
        'usage': mon.system_usage(),
        'services': mon.list_services()
    }


@app.get('/log')
def log(dep=Depends(verify_key)):
    with open(LOG_PATH) as f:
        lines = f.readlines()[-50:]
    return {'log': lines}


@app.post('/action/{service}')
def control_service(service: str, data: Action, dep=Depends(verify_key)):
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