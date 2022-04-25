#!/usr/bin/env bash
# This script runs the projects unit tests.

if [[ $(basename `pwd`) -ne "ServerMonitor" ]]; then
	echo "You've got to be in the ServerMonitor dir to run this script. "
	exit 
fi

if [[ -z $VIRTUAL_ENV ]]; then
	echo "You've got to source the venv before running this script."
	exit 
fi 

rm app/database.db

python -m pytest

