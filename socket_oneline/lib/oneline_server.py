import socket
import threading
import time


# --------------------
## holds the Oneline Server
class OnelineServer:
    # --------------------
    ## initialize
    def __init__(self):
        ## holds the IP Address for the socket
        self._ip_address = None
        ## holds the IP port for the socket
        self._ip_port = None
        ## holds the server socket
        self._server = None
        ## holds the incoming connection socket
        self._conn = None
        ## indicates if the server should still process incoming connections and commands
        self._is_done = False
        ## indicates if the server currently has a client connection
        self._is_connected = False
        ## the callback function to be used for an incoming command
        self._callback_fn = None
        ## the background thread to hold the socket processing
        self._thread = None
        ## a reference to the logger to use (if any)
        self._logger = None
        ## indicates logging verbosity, if False, no logging is done
        self._verbose = False

    # TODO add properties:
    #     ip_address=None,
    #     ip_port=None,
    #     callback=None,
    #     logger=None,
    #     verbose=None)

    # --------------------
    ## indicates if the server thread is still running
    #
    # @return True if the thread is alive, False otherwise
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    # --------------------
    ## starts the server using the given parameters
    #
    # @param ip_address  the IP address to listen on
    # @param ip_port     the IP port to listen on
    # @param callback    the callback function to use, None to use the default callback function
    # @param logger      the logger reference to use, None if no logging
    # @param verbose     if a logger is given and verbosity
    # @return None
    def start(self,
              ip_address: str = None,
              ip_port: int = None,
              callback=None,
              logger=None,
              verbose: bool = None):
        self._log('start')
        if ip_address is not None:
            self._ip_address = ip_address
        if ip_port is not None:
            self._ip_port = ip_port
        if callback is not None:
            self._callback_fn = callback
        if logger is not None:
            self._logger = logger
        if verbose is not None:
            self._verbose = verbose

        if not self._params_ok():
            return

        self._start_runner()

    # --------------------
    ## checks if the given parameters are set correctly
    #
    # @return True if all are set, False otherwise
    def _params_ok(self) -> bool:
        ok = True
        if self._ip_address is None:
            self._log(f'ERR  ip address is not set')
            ok = False
        if self._ip_port is None:
            self._log(f'ERR  ip port is not set')
            ok = False
        if self._callback_fn is None:
            ok = False
            self._log(f'ERR  callback is not set')
        return ok

    # --------------------
    ## start the bg thread to listen on the socket
    #
    # @return None
    def _start_runner(self):
        if self._thread is not None:
            # TODO it's already running
            # shut it down
            pass

        self._thread = threading.Thread(target=self._runner)
        self._thread.daemon = True
        self._thread.start()

        # wait for thread to start
        time.sleep(0.1)

    # --------------------
    ## send a response to the connected client
    #
    # @param rsp  the response packet to send
    # @return None
    def send(self, rsp: str):
        self._log(f'tx: {rsp}')
        # TODO check if _conn is not None
        self._conn.send(f'{rsp}\x0A'.encode())

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        self._log('terminate')
        self._is_connected = False
        self._is_done = True

        # wait for thread to end
        count = 0
        while self._thread.is_alive():
            count += 1
            if count > 3:
                break
            time.sleep(0.5)

        # if a connection is still up, unblock it
        if self._conn is not None:
            try:
                self._conn.send(b'')
            except (ConnectionAbortedError, BrokenPipeError):
                pass
        time.sleep(0.5)

        self._disconnect()
        self._server.close()

    # --------------------
    ## the bg thread runner that listens for a connection and handles the incoming client requests
    #
    # @return None
    def _runner(self):
        # TODO check if init called
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._log('thread started running')

        if not self._start_socket_listen():
            self._log(f'listen failed on {self._ip_address}:{self._ip_port}, exiting thread')
            self._is_done = True

        while not self._is_done:
            # continually wait for a connection from a PFC instance
            self._wait_for_connection()
            self._log('got connection')

            while self._is_connected and not self._is_done:
                cmd, is_invalid = self._recv()
                if cmd is None:
                    pass
                elif cmd == 'disconnect':
                    self._handle_disconnect()
                elif cmd == 'shutdown':
                    self._handle_shutdown()
                elif cmd == 'ping':
                    self._handle_ping()
                elif is_invalid:
                    self._handle_invalid(cmd)
                elif self._callback_fn is None:
                    self._default_callback_fn(cmd)
                else:
                    self._callback_fn(cmd)
                time.sleep(0.5)

            self._disconnect()

        # exiting thread, so clean up
        self._log('done, thread exiting')

    # --------------------
    ## Wait for incoming socket connection
    #
    # @return None
    def _wait_for_connection(self):
        self._log('waiting for a connection')
        self._server.settimeout(1.0)

        while not self._is_done and not self._is_connected:
            try:
                self._conn, _addr = self._server.accept()

                self._is_connected = True
                self._log(f'connection found via {_addr[0]}:{_addr[1]}')
                # got a connection, go handle it
            except socket.timeout:
                # go wait again
                pass
            except OSError as excp:
                # a normal exit request can cause this exception
                if not self._is_done:
                    # wasn't normal exit, so log it
                    self._log('accept() failed on OSError')
                    pass
                self._is_done = True

    # --------------------
    ## set up a listener for incoming connections
    #
    # @return True is the listener was correctly set up, False otherwise
    def _start_socket_listen(self):
        self._log('starting socket with listen')
        ok = True

        try:
            self._server.bind((self._ip_address, self._ip_port))
            self._server.listen(1)
        except socket.error:
            ok = False

        return ok

    # --------------------
    ## shutdown socket
    #
    # @return None
    def _disconnect(self):
        self._log('disconnecting')

        # release socket
        if self._conn is not None:
            if self._is_connected:
                self._log('still connected, shutting down socket')
                self._conn.shutdown(socket.SHUT_RDWR)

            self._conn.close()
            self._conn = None

        self._is_connected = False
        self._log('connection closed')

    # --------------------
    ## read incoming socket a byte at a time until newline is found
    #
    # @return None
    def _recv(self):
        cmd = ''
        is_invalid = False
        while True:
            if self._conn is None:
                break

            try:
                ch = self._conn.recv(1)
                if ch == b'\x0A':
                    break

                cmd += ch.decode()

            except UnicodeDecodeError:
                is_invalid = True
                self._log('decode excp occurred')
                cmd = None

            except (ConnectionAbortedError, OSError):
                self._is_connected = False
                self._is_done = True
                self._log('connection or OS error, closing connection and thread')
                cmd = None
                break

        self._log(f'rx: {cmd.strip()}')
        return cmd, is_invalid

    # --------------------
    ## handle a disconnect command; disconnects from current client
    #
    # @return None
    def _handle_disconnect(self):
        self._disconnect()

    # --------------------
    ## handle a shutdown command; disconnects and then exits thread loop
    #
    # @return None
    def _handle_shutdown(self):
        self._disconnect()
        self._is_done = True

    # --------------------
    ## handle a ping command; responds with 'pong'
    #
    # @return None
    def _handle_ping(self):
        self.send('pong')

    # --------------------
    ## handle an invalid command; currently just logs it
    #
    # @param cmd   the incoming command
    # @return None
    def _handle_invalid(self, cmd: str):
        self._log(f'handle invalid command "{cmd}"')

    # --------------------
    ## handle an incoming command; currently ignores it
    #
    # @param cmd   the incoming command
    # @return None
    def _default_callback_fn(self, cmd: str):
        # do nothing
        pass

    # --------------------
    ## log the message
    # if verbose is False, then nothing is logged
    # if verbose is True, and logger is defined, the msg is logged
    # if verbose is True, and logger is not defined, the msg is printed to stdout
    #
    # @param msg  the message to log
    # @return None
    def _log(self, msg):
        # handle verbose/quiet
        if not self._verbose:
            return

        buf = f'oneline srvr: {msg}'
        if self._logger is None:
            print(buf)
        else:
            self._logger.info(buf)
