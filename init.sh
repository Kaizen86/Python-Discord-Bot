#!/bin/bash
BOT_ID=Elizabeth

#Ensure current directory is set to script's location
cd "$(dirname "$0")"

if [[ $(screen -list | grep $BOT_ID) ]];
then
	echo "Aborted: Bot is already running."
else
	screen -dmS $BOT_ID /bin/bash screensession.sh
	echo "Started screen session."
fi
