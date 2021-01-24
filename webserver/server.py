import sys, signal
import http.server
import socketserver
from . import RangeRequestHandler

class Serve(object):
    def __init__(self,port):
        self.port = port

        # Note ForkingTCPServer does not work on Windows as the os.fork() 
        # function is not available on that OS. Instead we must use the 
        # subprocess server to handle multiple requests
        #self.server = socketserver.ThreadingTCPServer(('',self.port), http.server.SimpleHTTPRequestHandler )
        self.server = socketserver.ThreadingTCPServer(('',self.port), RangeRequestHandler)

        #Ensures that Ctrl-C cleanly kills all spawned threads
        self.server.daemon_threads = True  
        #Quicker rebinding
        self.server.allow_reuse_address = True  

        # Install the keyboard interrupt handler
        signal.signal(signal.SIGINT, self.signal_handler)

        # Now loop forever
        try:
            while True:
                sys.stdout.flush()
                self.server.serve_forever()
        except KeyboardInterrupt:
            pass

        self.server.server_close()

    
    # A custom signal handle to allow us to Ctrl-C out of the process
    def signal_handler(self, signal, frame):
        print( 'Exiting http server (Ctrl+C pressed)')
        try:
            if (self.server):
                self.server.server_close()
        finally:
            sys.exit(0)