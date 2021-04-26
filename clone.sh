#!/bin/bash

# pull the latest from the specified branch

if [ "$1" = "" ]; then
	echo "You must supply a release to pull"
	exit;
fi

git checkout $1 && git pull
