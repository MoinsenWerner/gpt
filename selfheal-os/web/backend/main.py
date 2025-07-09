import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from daemon.monitor import Monitor
from daemon.healer import Healer

app = FastAPI()
mon = Monitor()
healer = Healer()

# Pfad zur Logdatei
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs', 'events.log')

# Pfad zur index.html
INDEX_HTML = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/index.html'))

# Pfad zum statischen Verzeichnis (optional, falls du CSS/JS nutzt)
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

# Index-Datei unter "/"
@app.get("/")
def root():
    if os.path.exists(INDEX_HTML):
        return FileResponse(INDEX_HTML)
    else:
        raise HTTPException(status_code=404, detail="index.html not found")

# Optionale statische Dateien unter "/static/*"
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

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
        healer.kill_process(service)  # erwartet pid als string
    else:
        raise HTTPException(400, 'Unknown action')
    return {'status': 'ok'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=23673)
