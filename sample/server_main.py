import sys

sys.path.append('.')
from sample.server import Server
from sample.mock_logger import MockLogger
from sample.services import Services


# --------------------
## mainline
# runs the OnelineServer wrapper
def main():
    Services.logger = MockLogger()

    server = Server()
    server.init()

    server.wait_until_done()
    server.term()


# --------------------
if __name__ == '__main__':
    main()
