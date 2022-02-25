#!/bin/bash

# kill running "busses"
killall ${PWD}/src/venv/bin/python* 2> /dev/null

# Exit if something fails
# set -e

rm ~/.local/share/kservices5/me.itzvirtual.stringutils.desktop
rm ~/.local/share/dbus-1/services/me.itzvirtual.stringutils.service
kquitapp5 krunner
