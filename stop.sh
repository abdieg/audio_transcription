#!/bin/bash

SESSION="transcription"

if ! screen -list | grep -q "$SESSION"; then
    echo "App is not running"
    exit 1
fi

screen -S "$SESSION" -X quit
echo "Stopped (screen session '$SESSION')"
