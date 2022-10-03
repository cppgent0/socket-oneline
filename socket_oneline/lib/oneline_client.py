import socket


# --------------------
class OnelineClient:
    # --------------------
    def __init__(self):
        self._ip_address = None
        self._ip_port = None
        self._sock = None
        self._connected = False
        self._logger = None
        self._verbose = None

    # --------------------
    def init(self,
             ip_address: str = None,
             ip_port: int = None,
             logger=None,
             verbose: bool = None):
        if ip_address is not None:
            self._ip_address = ip_address
        if ip_port is not None:
            self._ip_port = ip_port
        if logger is not None:
            self._logger = logger
        if verbose is not None:
            self._verbose = verbose

        return self._params_ok()

    # --------------------
    def _params_ok(self) -> bool:
        ok = True
        if self._ip_address is None:
            self._log(f'ERR  ip address is not set')
            ok = False
        if self._ip_port is None:
            self._log(f'ERR  ip port is not set')
            ok = False
        return ok

    # --------------------
    # create and start tcp socket to OnelineServer
    #
    # @return True if connection worked ok, False otherwise
    def connect(self):
        if self._sock is not None:
            self.disconnect()

        # Create a socket (SOCK_STREAM means a TCP socket)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self._sock.connect((self._ip_address, self._ip_port))
            self._log(f'connected on {self._ip_address}:{self._ip_port}')
            self._connected = True
        except socket.error as excp:
            self._log(f'ERR connection failed on {self._ip_address}:{self._ip_port}')
            self._sock = None

        return self._connected

    # --------------------
    ## close the socket
    #
    # @return None
    def disconnect(self):
        if self._sock is None:
            self._log('already disconnected from server')
        else:
            if self._connected:
                self._sock.shutdown(socket.SHUT_RDWR)

            self._sock.close()
            self._sock = None

            self._log('disconnected from server')

        self._connected = False

    # --------------------
    ## send the given command to the OneLineServer
    #
    # @param cmd  the command to send
    # @return None
    def send(self, cmd):
        self._sock.sendall(f'{cmd}\x0A'.encode())

    # --------------------
    ## wait for a message from the OneLineServer
    #
    # @return if recv succeeded the received response, otherwise ''
    def recv(self):
        rsp = b''
        while True:
            try:
                ch = self._sock.recv(1)
                if ch == b'\x0A':
                    break
                rsp += ch
            except socket.timeout as e:
                # happens frequently, no need to log
                pass
            except (OSError, socket.error):
                self._log('socket failed. exiting thread')
                break

        rsp = rsp.decode()
        rsp = rsp.strip()
        return rsp

    # --------------------
    def _log(self, msg):
        # handle verbose/quiet
        if not self._verbose:
            return

        buf = f'oneline clnt: {msg}'
        if self._logger is None:
            print(buf)
        else:
            self._logger.info(buf)
