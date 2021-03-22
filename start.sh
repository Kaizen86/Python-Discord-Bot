#!/bin/sh
while true; do
	echo Starting bot...
	python3 bot.py
	echo Waiting 10 seconds before restarting.
	sleep 10
done
