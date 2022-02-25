#!/usr/bin/python3
import base64
import hashlib
from itertools import chain

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
        return hashlib.sha1(data).hexdigest()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def sha224(self, data: str):
        return hashlib.sha224(data).hexdigest()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def sha256(self, data: str):
        return hashlib.sha256(data).hexdigest()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def sha384(self, data: str):
        return hashlib.sha384(data).hexdigest()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def sha512(self, data: str):
        return hashlib.sha512(data).hexdigest()

    @dbus.service.method(iStringUtils, in_signature='s', out_signature='s')
    def md5(self, data: str):
        return hashlib.md5(data).hexdigest()


class KRunnerHandler(dbus.service.Object):
    ifaces = (Hashing, Encoding)

    def __init__(self):
        dbus.service.Object.__init__(self, dbus.service.BusName(iStringUtils, dbus.SessionBus()),
                                     "/krunnerhandler")

    @dbus.service.method(iKRunner, in_signature='s', out_signature='a(sssida{ss})')
    def Match(self, query: str):
        print("yes!")
        responses = []
        for iface in self.ifaces:
            for method in iface.methods:
                if query.startswith(method + " "):
                    try:
                        res = Hashing.__getattribute__(method)(query[len(method) + 1:])
                        response = krunner_response(res, res, {'subtext': 'Copy to Clipboard'})
                        if len(res > 10):
                            response = krunner_response(res, method, {'subtext': 'Copy to Clipboard'})
                        responses.append(response)
                    except Exception:
                        pass

    @dbus.service.method(iKRunner, out_signature='a(sss)')
    def Actions(self):
        # id, text, icon
        return [("id", "Copy", "edit-copy")]

    @dbus.service.method(iKRunner, in_signature='ss')
    def Run(self, data: str, action_id: str):
        print(data, "FROM RUN")


Encoding()
Hashing()
KRunnerHandler()
loop = GLib.MainLoop()
loop.run()
