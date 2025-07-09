#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"

# Start monitor and healer as background processes
python3 -m daemon.monitor &
MONITOR_PID=$!

# Start FastAPI backend
(cd "$DIR/web/backend" && uvicorn main:app --host 0.0.0.0 --port 23673) &
API_PID=$!

# Optionally start frontend
if [ "$1" = "--frontend" ]; then
  (cd "$DIR/web/frontend" && python3 -m http.server 3000) &
  FRONT_PID=$!
fi

trap 'kill $MONITOR_PID $API_PID $FRONT_PID 2>/dev/null' EXIT
wait
