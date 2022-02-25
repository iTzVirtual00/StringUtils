#!/bin/bash

# kill running "busses"
killall ${PWD}/src/venv/bin/python* 2> /dev/null

# Exit if something fails
# set -e

mkdir -p ~/.local/share/kservices5/
mkdir -p ~/.local/share/dbus-1/services/

cp me.itzvirtual.stringutils.desktop ~/.local/share/kservices5/
sed -e "s|%{INTERPRETER_PATH}|${PWD}/src/venv/bin/python|" \
    -e "s|%{SCRIPT_PATH}|${PWD}/src/stringutils.py|" \
    "me.itzvirtual.stringutils.service" > ~/.local/share/dbus-1/services/me.itzvirtual.stringutils.service

kquitapp5 krunner
