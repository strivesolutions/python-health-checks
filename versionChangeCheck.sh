#!/bin/bash

changes="$(git diff HEAD~1 HEAD pyproject.toml | grep 'version =')"

# echo "[ $changes ]"
if [ "$changes" != "" ]; then
    version="$(cat pyproject.toml | grep "version =" | cut -d"=" -f 2 | cut -d "\"" -f 2)"
    echo $version
fi
