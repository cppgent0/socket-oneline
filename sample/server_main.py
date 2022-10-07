import sys

sys.path.append('.')
from sample.mock_logger import MockLogger  # noqa: E402
from sample.services import Services  # noqa: E402
from sample.server import Server  # noqa: E402


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
