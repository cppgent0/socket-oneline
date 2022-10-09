from ver.core.ver_services import VerServices


# --------------------
## simulates a logger instance
class MockLogger:
    # --------------------
    ## initialize
    def __init__(self):
        ## holds the log lines as a list; used for UT or other testing
        self.lines = []

    # --------------------
    ## clear the lines array
    #
    # @return None
    def clear(self):
        self.lines = []

    # --------------------
    ## write the message to stdout and save to the array for later processing
    #
    # @param msg  the message to log
    # @return None
    def info(self, msg):
        if VerServices.verbose:
            print(f'INFO {msg}')
        self.lines.append(msg)
