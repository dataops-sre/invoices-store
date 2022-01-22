#!/bin/sh

echo "Waiting for MongoDB..."

python3 app_start_prehook.py

echo "MongoDB started"

python3 app.py
