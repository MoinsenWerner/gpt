#!/bin/bash
set -e
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd selfheal-os/web/frontend && npm install && cd ../../..
chmod +x selfheal-os/start.sh
echo "Installation complete. Activate venv with 'source venv/bin/activate'"
