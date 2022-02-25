#!/usr/bin/python3
import base64
import hashlib
import subprocess
import traceback
import uuid

import pyperclip

pyperclip.paste()  # from gi.repository import GLib is causing problems I didn't understand the problem, so I made
# pyperclip initialize the clipboard before importing it
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

from classes.utils import krunner_response

DBusGMainLoop(set_as_default=True)

iKRunner = "org.kde.krunner1"
iStringUtils = "me.itzvirtual.stringutils"


class Encoding(dbus.service.Object):
    methods = ('b85encode', 'b64encode', 'b32encode', 'b16encode', 'b85decode', 'b64decode', 'b32decode', 'b16decode')

    def __init__(self):
        dbus.service.Object.__init__(self, dbus.service.BusName(iStringUtils, dbus.SessionBus()),
                                     "/encoding")

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def b85encode(self, data: str):
        return base64.b85encode(data.encode()).decode()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def b64encode(self, data: str):
        return base64.b64encode(data.encode()).decode()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def b32encode(self, data: str):
        return base64.b32encode(data.encode()).decode()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def b16encode(self, data: str):
        return base64.b16encode(data.encode()).decode()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def b85decode(self, data: str):
        return base64.b85decode(data.encode()).decode()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def b64decode(self, data: str):
        return base64.b64decode(data.encode()).decode()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def b32decode(self, data: str):
        return base64.b32decode(data.encode()).decode()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def b16decode(self, data: str):
        return base64.b16decode(data.encode()).decode()


class Hashing(dbus.service.Object):
    methods = ('sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'md5')

    def __init__(self):
        dbus.service.Object.__init__(self, dbus.service.BusName(iStringUtils, dbus.SessionBus()),
                                     "/hashing")

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def sha1(self, data: str):
        return hashlib.sha1(data.encode()).hexdigest()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def sha224(self, data: str):
        return hashlib.sha224(data.encode()).hexdigest()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def sha256(self, data: str):
        return hashlib.sha256(data.encode()).hexdigest()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def sha384(self, data: str):
        return hashlib.sha384(data.encode()).hexdigest()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def sha512(self, data: str):
        return hashlib.sha512(data.encode()).hexdigest()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def md5(self, data: str):
        return hashlib.md5(data.encode()).hexdigest()


class Utils(dbus.service.Object):
    methods = ('len', 'uuid4')

    def __init__(self):
        dbus.service.Object.__init__(self, dbus.service.BusName(iStringUtils, dbus.SessionBus()),
                                     "/utils")

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def len(self, data: str):
        return str(len(data))

    @dbus.service.method(iStringUtils, out_signature='s')
    def uuid4(self,
              *args):  # I need to use *args because it is getting harder to add features (my code just sucks rn)
        return uuid.uuid4().hex


class KRunnerHandler(dbus.service.Object):
    ifaces = (Encoding(), Hashing(), Utils())
    emptyness = []  # dont ask

    def __init__(self):
        dbus.service.Object.__init__(self, dbus.service.BusName(iStringUtils, dbus.SessionBus()),
                                     "/krunnerhandler")

    @dbus.service.method(iKRunner, in_signature='s', out_signature='a(sssida{sv})')
    def Match(self, query: str):
        for iface in self.ifaces:
            for method in iface.methods:
                if query.startswith(method + " "):
                    try:
                        result = iface.__getattribute__(method)(query[len(method) + 1:])
                        response = krunner_response(result, method + "(): " + result)
                        if len(result) > 20:
                            response = krunner_response(result, 'copy result of ' + method + "()")
                        return [response]
                    except Exception:
                        # traceback.print_exc()
                        ...
        return self.emptyness

    @dbus.service.method(iKRunner, out_signature='a(sss)')
    def Actions(self):
        # id, text, icon
        return [("id", "Copy to Clipboard", "edit-copy")]

    @dbus.service.method(iKRunner, in_signature='ss')
    def Run(self, data: str, action_id: str):
        pyperclip.copy(data)


KRunnerHandler()
loop = GLib.MainLoop()
loop.run()
