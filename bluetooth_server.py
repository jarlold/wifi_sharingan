#!/usr/bin/python
import argparse
import sys
import os
import time
from bluetooth import *

# Main loop
def main():
    # We need to wait until Bluetooth init is done
    time.sleep(10)

    # Make device visible
    os.system("hciconfig hci0 piscan")

    # Create a new server socket using RFCOMM protocol
    server_sock = BluetoothSocket(RFCOMM)
    # Bind to any port
    server_sock.bind(("", PORT_ANY))
    # Start listening
    server_sock.listen(1)

    # Get the port the server socket is listening
    port = server_sock.getsockname()[1]

    # The service UUID to advertise
    uuid = "7be1fcb3-5776-42fb-91fd-2ee7b5bbb86d"

    # Start advertising the service
    advertise_service(server_sock, "RaspiBtSrv",
                       service_id=uuid,
                       service_classes=[uuid, SERIAL_PORT_CLASS],
                       profiles=[SERIAL_PORT_PROFILE])

    # These are the operations the service supports
    # Feel free to add more
    operations = ["ping", "example"]

    # Main Bluetooth server loop
    while True:

        print "Waiting for connection on RFCOMM channel %d" % port

        try:
            client_sock = None

            # This will block until we get a new connection
            client_sock, client_info = server_sock.accept()
            print "Accepted connection from ", client_info

            client_sock.send("connectified!\r\n")

            # Read the data sent by the client
            data = client_sock.recv(1024)
            if len(data) == 0:
                break

            print "Received [%s]" % data

            # Handle the request
            if data == "getop":
                response = "op:%s" % ",".join(operations)
            elif data == "ping":
                response = "msg:Pong"
            elif data == "example":
                response = "msg:This is an example"
            # Insert more here
            else:
                response = "msg:Not supported"

            client_sock.send(response)
            print "Sent back [%s]" % response

        except IOError:
            pass

        except KeyboardInterrupt:

            if client_sock is not None:
                client_sock.close()

            server_sock.close()

            print "Server going down"
            break
