#/bin/bash
source ~/Documents/scripts/testing-notifier/.venv/bin/activate
python userbrain.py tom > logs/userbrain-t.log & echo $!
#python userbrain.py kristine > logs/userbrain-k.log & echo $!
python usertesting.py tom > logs/usertesting-t.log & echo $!
#python usertesting.py kristine > logs/usertesting-k.log & echo $!
