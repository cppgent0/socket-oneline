import sys

sys.path.append('.')
from sample.logger import Logger  # noqa: E402
from sample.services import Services  # noqa: E402
from sample.server import Server  # noqa: E402


# --------------------
## mainline
# runs the OnelineServer wrapper
def main():
    Services.logger = Logger()

    server = Server()
    server.init()

    server.wait_until_done()
    server.term()


# --------------------
if __name__ == '__main__':
    main()
