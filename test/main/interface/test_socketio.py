# -*- coding: utf-8 -*-

import logging
import better_exceptions
from socketIO_client import SocketIO, LoggingNamespace

from swagger_client.main.configuration import Configuration
config = Configuration()
better_exceptions.MAX_LENGTH = None


class TestWS:
    def ignoretest_depath(self):
        def on_depth(*args):
            # TODO assert res struct
            print(args)

        with SocketIO('ws://crush-websocket-publisher.crush-deploy.lan', 80, LoggingNamespace) as socketio:
            socketio.on('crush/depth', on_depth)

    def test_kline(self):
        def on_kline(*args):
            print(args)

        with SocketIO('ws://crush-websocket-publisher.crush-deploy.lan', 80, LoggingNamespace) as socketio:
            # socketio.on('crush/k-line', on_kline)
            socketio.emit('crush/k-line', {"tradeingAreaId": '1', "period": "12h", "roomKey": 'kline-room-1-12h'}, on_kline)
            socketio.wait(seconds=1)
