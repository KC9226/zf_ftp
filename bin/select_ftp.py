# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZF


from sys import path
path.append(r'../modules')
# from classes import *
from classes import Feature
import selectors
import socket
import json

sel = selectors.DefaultSelector()


def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn, mask):
    recv_data = conn.recv(1000)  # Should be ready
    if recv_data:
            print('echoing', repr(recv_data), 'to', conn)
            data = json.loads(recv_data.decode())
            action = data.get("action")
            if hasattr(Feature, action):
                    func = getattr(Feature, action)
                    func(data, conn)
            else:
                    print("task action is not supported", action)
    else:
            print('closing', conn)
            sel.unregister(conn)
            conn.close()

sock = socket.socket()
sock.bind(('localhost', 10000))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)


while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
