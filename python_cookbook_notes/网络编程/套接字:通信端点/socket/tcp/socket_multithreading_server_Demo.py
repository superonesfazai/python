#!/usr/bin/env python
# coding=utf-8

from socketserver import ThreadingTCPServer, StreamRequestHandler
import traceback

class MyStreamRequestHandler(StreamRequestHandler):
    def handle(self):
        while True:
            try:
                data = self.rfile.readline().strip()
                print("receive from (%r):%r" % (self.client_address, data))
                self.wfile.write(data.upper() + '\n')
            except:
                traceback.print_exc()
                break

if __name__ == '__main__':
    host = ''  #主机名,可以是ip,像localhost的主机名,或""
    port = 8201
    addr = (host, port)

    #ThreadingTCPServer从ThreadingMixIn和TCPServer继承
    #class ThreadingTCPServer(ThreadingMixIn, TCPServer):pass
    server = ThreadingTCPServer(addr, MyStreamRequestHandler)
    server.serve_forever()
