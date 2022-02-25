#!/usr/bin/python3
import subprocess

import dbus.service
# import pyperclip
import os
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

from classes.handlers import KRunnerHandler

DBusGMainLoop(set_as_default=True)

objpath = "/stringutils"

iface = "org.kde.krunner1"


def klipper_copy(text):
    p = subprocess.Popen(
        ['qdbus', 'org.kde.klipper', '/klipper', 'setClipboardContents',
         text.encode()],
        stdin=subprocess.PIPE, close_fds=True)
    p.communicate(input=None)


class Runner(dbus.service.Object):
    def __init__(self):
        dbus.service.Object.__init__(self, dbus.service.BusName("me.itzvirtual.stringutils", dbus.SessionBus()),
                                     objpath)

    @dbus.service.method(iface, in_signature='s', out_signature='a(sssida{sv})')
    def Match(self, query: str):
        return KRunnerHandler.forward(query)

    @dbus.service.method(iface, out_signature='a(sss)')
    def Actions(self):
        # id, text, icon
        return [("id", "Copy", "edit-copy")]

    @dbus.service.method(iface, in_signature='ss')
    def Run(self, data: str, action_id: str):
        print(action_id)
        klipper_copy(data)


runner = Runner()
loop = GLib.MainLoop()
loop.run()
