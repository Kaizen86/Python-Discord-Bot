@echo off
color a
title Bot Bootloader
cls

echo Starting...
start "Wheatley Discord Bot" /d "%~dp0" "%~dp0\bot_files\bot.exe"
