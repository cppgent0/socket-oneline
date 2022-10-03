import sys

sys.path.append('.')
from sample.mock_logger import MockLogger
from sample.server import Server
from sample.client import Client
from sample.services import Services


# --------------------
def main():
    Services.logger = MockLogger()

    # TODO handle Ctrl-C
    # TODO start server as a Popen process
    # TODO check if server came down cleanly or threw excp; how?
    server = Server()
    server.init()

    # server is up, talk to it with a client
    client = Client()
    client.init()

    cmd = 'ping'
    Services.logger.info(f'main   : tx: {cmd}')
    client.send(cmd)
    rsp = client.recv()
    Services.logger.info(f'main   : rx: {rsp}')

    cmd = 'cmd01'
    Services.logger.info(f'main   : tx: {cmd}')
    client.send(cmd)
    rsp = client.recv()
    Services.logger.info(f'main   : rx: {rsp}')

    cmd = 'junk'
    Services.logger.info(f'main   : tx: {cmd}')
    client.send(cmd)
    rsp = client.recv()
    Services.logger.info(f'main   : rx: {rsp}')

    cmd = 'quit'
    Services.logger.info(f'main   : tx: {cmd}')
    client.send(cmd)

    client.term()

    # # create a new client
    # client = Client()
    # client.init()
    #
    # cmd = 'ping'
    # Services.logger.info(f'main   : tx: {cmd}')
    # client.send(cmd)
    # rsp = client.recv()
    # Services.logger.info(f'main   : rx: {rsp}')
    #
    # cmd = 'quit'
    # Services.logger.info(f'main   : tx: {cmd}')
    # client.send(cmd)
    #
    # client.term()

    server.wait_until_done()
    server.term()


# --------------------
if __name__ == '__main__':
    main()
