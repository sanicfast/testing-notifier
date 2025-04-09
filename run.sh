#/bin/bash
source ~/Documents/scripts/testing-notifier/.venv/bin/activate
python userbrain.py tom & echo $!
#python userbrain.py kristine & echo $!
python usertesting.py tom & echo $!
#python usertesting.py kristine & echo $!
