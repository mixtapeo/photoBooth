#!/usr/bin/env bash
set -e

echo "Installing system dependencies…"
sudo apt-get update
sudo apt-get install -y gphoto2

echo "Installing Python dependencies…"
pip install -r requirements.txt

echo "Done."