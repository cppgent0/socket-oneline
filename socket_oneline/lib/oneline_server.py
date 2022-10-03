import socket
import threading
import time


# --------------------
class OnelineServer:
    # --------------------
    def __init__(self):
        self._ip_address = None
        self._ip_port = None
        self._server = None
        self._conn = None
        self._is_done = False
        self._is_connected = False
        self._callback_fn = None
        self._thread = None
        self._logger = None
        self._verbose = False

    # TODO add properties:
    #     ip_address=None,
    #     ip_port=None,
    #     callback=None,
    #     logger=None,
    #     verbose=None)

    # --------------------
    def is_running(self):
        return self._thread is not None and self._thread.is_alive()

    # --------------------
    def start(self, ip_address=None, ip_port=None, callback=None, logger=None, verbose=None):
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
    def _params_ok(self):
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
    ## terminate
    #
    # @return None
    def term(self):
        self._log('oneline: terminate')
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
    def _runner(self):
        # TODO check if init called
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._log('oneline: thread started runing')

        if not self._start_socket_listen():
            self._log(f'oneline: listen failed on {self._ip_address}:{self._ip_port}, exiting thread')
            self._is_done = True

        while not self._is_done:
            # continually wait for a connection from a PFC instance
            self._wait_for_connection()
            self._log('oneline: got connection')

            while self._is_connected and not self._is_done:
                cmd, is_invalid = self._recv()
                if cmd is None:
                    pass
                elif cmd == 'quit':
                    self._handle_quit(cmd)
                elif cmd == 'ping':
                    self._handle_ping(cmd)
                elif is_invalid:
                    self._handle_is_invalid(cmd)
                elif self._callback_fn is None:
                    self._default_callback_fn(cmd)
                else:
                    self._callback_fn(cmd)
                time.sleep(0.5)

            self._disconnect()

        # exiting thread, so clean up
        self._log('oneline: done, thread exiting')

    # --------------------
    ## Wait for incoming socket connection
    #
    # @return None
    def _wait_for_connection(self):
        self._log('oneline: waiting for a connection')
        self._server.settimeout(1.0)

        # self._set_initial_state()
        while not self._is_done and not self._is_connected:
            try:
                self._conn, self._addr = self._server.accept()

                self._is_connected = True
                self._log(f'oneline: connection found via {self._addr[0]}:{self._addr[1]}')
                # got a connection, go handle it
            except socket.timeout:
                # go wait again
                pass
            except OSError as excp:
                # a normal exit request can cause this exception
                if not self._is_done:
                    # wasn't normal exit, so log it
                    self._log('oneline: accept() failed on OSError')
                    pass
                self._is_done = True
                # self._set_initial_state()

    # --------------------
    def _start_socket_listen(self):
        self._log('oneline: Starting socket with listen')
        result = True

        try:
            self._server.bind((self._ip_address, self._ip_port))
            self._server.listen(1)
        except socket.error as excp:
            result = False

        return result

    # --------------------
    ## shutdown socket
    #
    # @return None
    def _disconnect(self):
        self._log('oneline: disconnecting')

        # release socket
        if self._conn is not None:
            if self._is_connected:
                self._log('oneline: still connected, shutting down socket')
                self._conn.shutdown(socket.SHUT_RDWR)

            self._conn.close()
            self._conn = None
        self._log('oneline: connection closed')

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
                ch = self._conn.recv(1).decode()
                if ch == 0x0A:
                    cmd += ch
                    break

                cmd += ch

            except UnicodeDecodeError:
                is_invalid = True
                self._log('oneline: decode excp occurred')
                cmd = None

            except (ConnectionAbortedError, OSError):
                self._is_connected = False
                self._is_done = True
                self._log('oneline: connection or OS error, closing connection and thread')
                cmd = None
                break

        self._log(f'rx: {cmd.strip()}')
        return cmd, is_invalid

    # --------------------
    def _send(self, rsp):
        self._log(f'tx: {rsp}')
        self._conn.send(f'{rsp}\x0A'.encode())

    # --------------------
    def _handle_quit(self, cmd):
        self._log('oneline: received quit')
        self._disconnect()

    # --------------------
    def _handle_ping(self, cmd):
        self._log('oneline: received ping')
        self._send('pong')

    # --------------------
    def _handle_is_invalid(self, cmd):
        self._log('oneline: handle invalid command')
        pass

    # --------------------
    def _default_callback_fn(self, cmd):
        # do nothing
        pass

    # --------------------
    def _log(self, msg):
        # handle verbose/quiet
        if not self._verbose:
            return

        if self._logger is None:
            print(msg)
        else:
            self._logger.info(msg)
