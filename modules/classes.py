# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZF

import socket
import selectors
import os, sys
import json


class Feature:
    @staticmethod
    def ls(data, conn):
        list = os.listdir('./')
        conn.send(bytes(json.dumps(list), encoding='utf-8'))

    @staticmethod
    def get(data, conn):
        pass

    @staticmethod
    def put(data, conn):
        conn.send(bytes('True', encoding='utf-8'))
        filesize = data["filesize"]
        filename = data["filename"]
        print(filename, filesize)
        f = open(filename, 'wb')
        recv_size = 0
        while recv_size < filesize:
            data = conn.recv(4096)
            f.write(data)
            recv_size += len(data)
        print('file recv success')
        f.close()
