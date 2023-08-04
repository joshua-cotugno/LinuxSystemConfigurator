#!/bin/bash

architecture=''

if [ '$(uname -m)' = 'x86_64' ] || [ '$(uname -m)' = 'amd64' ]; then
    architecture='amd64'
elif [ '$(uname -m)' = 'aarch64' ]; then
    architecture='aarch64'
fi

echo '$architecture'