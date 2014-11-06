#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 \"commit words\""
    exit 0
fi

git add *
git commit -m "$1"
git push origin master

