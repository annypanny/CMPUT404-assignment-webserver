#! /usr/bin/env python
#  coding: utf-8
#
import SocketServer
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


# status code
# https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html


class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall("OK")
        # split date into a list
        data_split = self.data.split()
        # get command, uri and version from list
        command = data_split[0]
        uri = data_split[1]
        version = data_split[2]
        # find folder www's path
        path = os.path.abspath(uri)
        path_root = os.path.abspath("www")

        # only files in ./www and deeper to be served
        if "../" in uri:
            response = "HTTP/1.1 404 Not Found\r\n"
            content = """\
                    <!DOCTYPE html>
                    <html>
                    <body>
                    <h1>HTTP/1.1 404 Not Found</h1>
                    </body>
                    </html>
                    """
            response += content + "\r\n\r\n"
            self.request.sendall(response)

        # add index.html at end
        elif uri[-1] == "/":
            path = os.path.abspath(path_root+path+ "/index.html")
            #print path

        else:
            path += path_root
            #print path





        if (command == "GET"):
            try:
                f = open(path,'r')
                fdata = f.read()
                mime=""
                # check mime type HTML or CSS
                if uri.split('.')[-1].lower() == "html":
                    mime = "text/html"
                elif uri.split('.')[-1].lower()== "css":
                    mime = "text/css"

                response = "HTTP/1.1 200 OK\r\n"
                response += "Content-Length:"+ str(len(fdata)) +"\r\n"
                response += "Content-Type:"+ str(mime) +"\r\n"
                        #'Connection: close'
                content = """\
                        <!DOCTYPE html>
                        <html>
                        <body>
                        <h1>HTTP/1.1 200 OK</h1>
                        </body>
                        </html>
                        """
                response += content + "\r\n\r\n"
                self.request.sendall(response)
                self.request.sendall(fdata)



            except Exception as e:
                response = "HTTP/1.1 404 Not Found\r\n"
                content = """\
                        <!DOCTYPE html>
                        <html>
                        <body>
                        <h1>HTTP/1.1 404 Not Found</h1>
                        </body>
                        </html>
                        """
                response += content + "\r\n\r\n"
                self.request.sendall(response)
        else:
            response = "HTTP/1.1 501 Not Implemented\r\n"
            content = """\
                    <!DOCTYPE html>
                    <html>
                    <body>
                    <h1>HTTP/1.1 501 Not Implemented</h1>
                    <p>The server does not support the functionality
                    required to fulfill the request.
                    Please use GET to request.</p>
                    </body>
                    </html>
                    """
            response += content + "\r\n\r\n"
            self.request.sendall(response)




if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    #server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
