@setlocal enableextensions enabledelayedexpansion
@echo off
title Bot compiler

REM A list of bot config files to be included
set configfiles=admins.config bot.config commands.config
REM What directory should the compiled bot be placed?
set outputfolder=Wheatley-Compiled
REM What file should PyInstaller attempt to package?
set compiletarget=bot.py

echo COMPILING BOT...
pyinstaller %compiletarget%

echo RENAMING SUBFOLDER...
set subfolder=!compiletarget:~0,-3!
rename %outputfolder%\%subfolder% %outputfolder%\%subfolder%_files

echo DELETING JUNK FILES...
set x=__pycache__ build
for %%a in (%x%) do (
	echo - %%a
	rmdir /s /q %%a
)

REM Delete  all *.spec files
FOR %%a in (*.spec) do (
	echo - %%a 
	del %%a
)

echo RENAMING dist/ TO %outputfolder%/
rename dist %outputfolder%

echo COPYING CONFIG FILES...
for %%a in (%configfiles%) do (
	copy %%a %outputfolder%
)

echo COPYING ADDITIONAL BOT RESOURCES...

xcopy /e bot_files %outputfolder%\%subfolder%\
xcopy /e Post_Compile %outputfolder%\

echo DONE!
pause