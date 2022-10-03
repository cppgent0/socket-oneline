import time

from sample.services import Services
from socket_oneline.lib.oneline_server import OnelineServer


# --------------------
class Server:
    # --------------------
    def __init__(self):
        self._server = OnelineServer()

    # --------------------
    def init(self):
        Services.logger.info('server : started')

        self._server.start(ip_address=Services.ip_address,
                           ip_port=Services.ip_port,
                           callback=self._callback,
                           logger=Services.logger,
                           verbose=Services.verbose)
        time.sleep(0.1)

    # --------------------
    def wait_until_done(self):
        while self._server.is_running():
            time.sleep(0.5)

    # --------------------
    def _callback(self, cmd):
        Services.logger.info(f'server : callback: cmd="{cmd}"')
        if cmd == 'cmd01':
            self._server.send('ack')
        else:
            self._server.send('nak')

    # --------------------
    def term(self):
        pass
