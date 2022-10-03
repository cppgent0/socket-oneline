import time

from sample.services import Services
from socket_oneline.lib.oneline_server import OnelineServer


# --------------------
class Server:
    # --------------------
    def __init__(self):
        self._cfg = None
        self._server = OnelineServer()

    # --------------------
    def init(self):
        Services.logger.info('server: started')

        self._server.start(ip_address=Services.ip_address,
                           ip_port=Services.ip_port,
                           callback=self._callback,
                           logger=Services.logger,
                           verbose=True)
        time.sleep(0.1)

    # --------------------
    def wait_until_done(self):
        while self._server.is_running():
            time.sleep(0.5)

    # --------------------
    def _callback(self, cmd):
        Services.logger.info(f'server: callback: cmd="{cmd}"')

    # --------------------
    def term(self):
        pass
