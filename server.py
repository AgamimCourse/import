#! /usr/bin/env python

from SocketServer import TCPServer, ForkingMixIn, BaseRequestHandler
import argparse

AGAMIM_FILE = "agamim.txt"
DEFAULT_MESSAGE = [
    "A true Agamist never stops trying!\n",
    ]

class AgamimRequestHandler(BaseRequestHandler):
    def handle(self):
        try:
            with open(AGAMIM_FILE, "rb") as file_:
                lines = file_.readlines()
        except IOError:
            lines = DEFAULT_MESSAGE

        for line in lines:
            self.request.sendall("%s" % (line, ))

    def finish(self):
        self.request.shutdown(0)
        self.request.close()

class AgamimServer(ForkingMixIn, TCPServer):
    def __init__(self, (host, port), request_handler):
        self.allow_reuse_address = True
        TCPServer.__init__(self, (host, port), request_handler)

def _parse_arguments():
    parser = argparse.ArgumentParser(
        description = "Start an Agamim message server for 'import agamim'.")

    parser.add_argument(
        "--host",
        default = "localhost",
        help = "Server's host address")

    parser.add_argument(
        "port",
        type = int,
        help = "Server's listening port")

    return parser.parse_args()

def run():
    arguments = _parse_arguments()

    server = AgamimServer(
        (arguments.host, arguments.port),
        AgamimRequestHandler)

    server.serve_forever()

if "__main__" == __name__:
    exit(run())
