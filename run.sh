#!/bin/bash
cd /home/tom/Documents/scripts/testing-notifier
export PYTHONUNBUFFERED=1
source .venv/bin/activate
python userbrain.py tom > logs/userbrain-t.log 2>&1 & echo $!
python usertesting.py tom > logs/usertesting-t.log 2>&1 & echo $!
python userbrain.py kristine > logs/userbrain-k.log 2>&1 & echo $!
python usertesting.py kristine > logs/usertesting-k.log 2>&1 & echo $!
pkill chrome
