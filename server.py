#! /usr/bin/env python

from SocketServer import TCPServer, ForkingMixIn, BaseRequestHandler
import socket
import fcntl
import struct
import logging
import argparse

SIOCGIFADDR = 0x8915
LOG_FILE = "agamim.log"
AGAMIM_FILE = "agamim.txt"
DEFAULT_MESSAGE = [
    "A true Agamist never stops trying!\n",
    ]

def _get_ip_from_interface(interface):
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        address = fcntl.ioctl(
            temp_socket.fileno(),
            SIOCGIFADDR,
            struct.pack('256s', interface[:15]))
    except IOError:
        return "127.0.0.1"

    return socket.inet_ntoa(address[20:24])

class AgamimRequestHandler(BaseRequestHandler):
    def handle(self):
        (peer_ip, peer_port) = self.request.getpeername()
        logging.info("Getting request from %s:%d", peer_ip, peer_port, )

        try:
            with open(AGAMIM_FILE, "rb") as file_:
                lines = file_.readlines()
        except IOError:
            logging.warning("Failed to read file '%s'", AGAMIM_FILE)
            lines = DEFAULT_MESSAGE

        logging.info("Sending message")
        for line in lines:
            self.request.sendall("%s" % (line, ))
        logging.info("Message sent")

    def finish(self):
        self.request.shutdown(0)
        self.request.close()
        logging.info("Closed connection with peer")

class AgamimServer(ForkingMixIn, TCPServer):
    def __init__(self, (host, port), request_handler):
        self.allow_reuse_address = True
        TCPServer.__init__(self, (host, port), request_handler)

def _parse_arguments():
    parser = argparse.ArgumentParser(
        description = "Start an Agamim message server for 'import agamim'.")

    parser.add_argument(
        "--iface",
        default = "eth0",
        help = "Server's interface (used to resolve IP)")

    parser.add_argument(
        "port",
        type = int,
        help = "Server's listening port")

    return parser.parse_args()

def run():
    arguments = _parse_arguments()
    (ip, port) = (_get_ip_from_interface(arguments.iface), arguments.port)

    # Setup logging.
    logging.basicConfig(
        filename = LOG_FILE,
        format = "%(levelname)s:%(process)d:%(message)s",
        level = logging.INFO)

    server = AgamimServer((ip, port), AgamimRequestHandler)

    logging.info("Starting server on %s:%d", ip, port)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Stopped by user")

if "__main__" == __name__:
    exit(run())
