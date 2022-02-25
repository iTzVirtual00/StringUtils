#!/bin/bash

# kill running busses
killall ${PWD}/src/venv/bin/python* 2> /dev/null

# Exit if something fails
# set -e

rm ~/.local/share/kservices5/plasma-runner-stringutils.desktop
rm ~/.local/share/dbus-1/services/org.kde.stringutils.service
kquitapp5 krunner
