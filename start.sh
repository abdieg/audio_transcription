#!/bin/bash

SESSION="transcription"

if screen -list | grep -q "$SESSION"; then
    echo "App is already running (screen session '$SESSION')"
    exit 1
fi

TAILSCALE_IP=$(tailscale ip -4 2>/dev/null)
if [ -z "$TAILSCALE_IP" ]; then
    echo "Tailscale is not running or has no IP"
    exit 1
fi

screen -dmS "$SESSION" uv run streamlit run app.py --server.address "$TAILSCALE_IP" --server.port 10050
echo "Started on http://$TAILSCALE_IP:10050 (screen session '$SESSION')"
