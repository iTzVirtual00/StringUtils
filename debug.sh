mkdir -p ~/.local/share/kservices5/
cp me.itzvirtual.stringutils.desktop ~/.local/share/kservices5/
killall ${PWD}/src/venv/bin/python* 2> /dev/null
kquitapp5 krunner
src/venv/bin/python src/stringutils.py