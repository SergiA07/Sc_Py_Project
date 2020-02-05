import socket
import threading
from analyser import FeatureAnalyser
from server_REST import server_REST
from server_OSC import server_OSC


class serverThread (threading.Thread):
    def __init__(self, server, analysis, name="threadName"):
        threading.Thread.__init__(self)
        self.server = server
        self.name = name
        self.analysis = analysis

    def run(self):
        print("Starting " + self.name)
        self.server(self.analysis)
        print("Exiting " + self.name)


if __name__ == "__main__":
    analysis = FeatureAnalyser()

    # Create server threads
    test_analysis_for_REST = {"keytest": 1234}
    thread1 = serverThread(
        server_REST, test_analysis_for_REST, "Thread-REST-server")
    thread2 = serverThread(server_OSC, analysis, "Thread-OSC-server")

    # Start new Threads
    thread1.start()
    thread2.start()

    print("Exiting Main Thread")
