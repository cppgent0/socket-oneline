import sys

sys.path.append('.')
from sample.mock_logger import MockLogger
from sample.server import Server
from sample.services import Services


# --------------------
def main():
    Services.logger = MockLogger()

    # TODO handle Ctrl-C

    server = Server()
    server.init()

    # TODO do something with Client

    server.wait_until_done()
    server.term()


# --------------------
if __name__ == '__main__':
    main()
