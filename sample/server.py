import time

from sample.services import Services
from socket_oneline.lib.oneline_server import OnelineServer


# --------------------
## sample Server that wraps the OnelineServer
class Server:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds reference to the Oneline Server
        self._server = OnelineServer()

    # --------------------
    ## initialize
    # Start the OnelineServer
    #
    # @return None
    def init(self):
        Services.logger.info('server      : started')

        self._server.start(ip_address=Services.ip_address,
                           ip_port=Services.ip_port,
                           callback=self._callback,
                           logger=Services.logger,
                           verbose=Services.verbose)
        # TODO convert to wait_until... with timeout
        time.sleep(0.1)

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        pass

    # --------------------
    ## wait until the server stops running i.e. it is shutdown
    #
    # @return None
    def wait_until_done(self):
        while self._server.is_running():
            time.sleep(0.5)

    # --------------------
    ## callback function used by OnelineServer to handle incoming commands
    #
    # @param cmd  the incoming command from the client
    # @return None
    def _callback(self, cmd):
        Services.logger.info(f'server      : callback: cmd="{cmd}"')
        if cmd == 'cmd01':
            self._server.send('ack')
        else:
            # unknown command, let client know
            self._server.send('nak - unknown cmd')
