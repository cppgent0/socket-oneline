import time

from sample.services import Services
from socket_oneline.lib.oneline_client import OnelineClient


# --------------------
class Client:
    # --------------------
    def __init__(self):
        self._client = OnelineClient()

    # --------------------
    def init(self):
        Services.logger.info('client : started')

        ok = self._client.init(ip_address=Services.ip_address,
                               ip_port=Services.ip_port,
                               logger=Services.logger,
                               verbose=Services.verbose)

        if ok:
            self._client.connect()
            # TODO replace with wait_until... with timeout
            time.sleep(0.1)

    # --------------------
    def term(self):
        self._client.disconnect()
        self._client = None

    # --------------------
    def send(self, cmd):
        self._client.send(cmd)

    # --------------------
    def recv(self):
        rsp = self._client.recv()
        return rsp

    # --------------------
    def term(self):
        pass
