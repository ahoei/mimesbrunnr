#!/bin/bash

if [ ! -f ~/.initialized ]; then
    git config --local --add --bool push.autoSetupRemote true
    git config --local core.editor 'code --wait'
    git config --local push.default current

    touch ~/.initialized
fi
