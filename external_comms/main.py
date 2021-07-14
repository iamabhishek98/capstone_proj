from eval_client import Client
from ultra96_server import Server
from dashboard_server import Dashboard_Server
import sys
import time
import threading
from statistics import mean

REMOTE_SERVER = True

# Runs Ultra96_server, dashboard_server and eval_client
class ultra96():
    def __init__(self):
        # Threading
        self.dancer_data_lock = threading.Lock()
        self.logout = threading.Event()
        self.dancers_ready = threading.Event()
        self.dashboard_ready = threading.Event()

        # IP
        ULTRA_SERVER_ADDR = ('localhost', 8081)
        EVAL_SERVER_ADDR = ("localhost", 9003)
        DASHBOARD_SERVER_ADDR = ("localhost", 8083)

        # Config
        NUM_OF_DANCERS = 1
        SYNC_THRESHOLD = 0.2 # Week 7 dummy data
        BUFF_SIZE = 256
        SECRET_KEY = 9999999999999999
        
        # Initialise Ultra96_server, dashboard_server and eval_client
        self.server = Server(ULTRA_SERVER_ADDR, SECRET_KEY, ultra96=self,
                             sync_threshold=SYNC_THRESHOLD, buff_size=BUFF_SIZE, dancers_count=NUM_OF_DANCERS)
        classEng = self.server.classifier
        self.eval_client = Client(EVAL_SERVER_ADDR, SECRET_KEY, ultra96=self, classifier = classEng)
        self.dashboard_server = Dashboard_Server(
            DASHBOARD_SERVER_ADDR, SECRET_KEY, dashboard_ready=self.dashboard_ready, buff_size=BUFF_SIZE)

        # Variables to handle the data
        self.has_evaluated = True
        self.sync_delay = 0
        self.first_x_timestamp = {}
        self.sync_evaluated = False
        self.pos = [1, 2, 3] # Week 7 dummy data

    # Starts the program and creates relevant threads
    def start(self):
        dashboard_conn_thread = threading.Thread(
            target=self.dashboard_server.start, args=())
        dashboard_conn_thread.setDaemon(True)
        dashboard_conn_thread.start()
        self.server.setDaemon(True)
        self.server.start()

        # Keeps polling until all required connections are setup
        while True:
            # self.dashboard_ready.wait()
            self.dancers_ready.wait()

            # To ensure connections are setup before connecting to eval_server
            if self.dancers_ready.is_set():
                time.sleep(0.5)
                print("Dancers Connected....")
                print("Start Dance Engine....")
                start_command = input(
                    "Press any key after dancer all Dancers connected[Y/N]")
                self.server.start_evaluation()

                start_command = input(
                    "Do you wish to connect to eval server and start the run? [Y/N]")
                if start_command.lower() == "y":
                    break
        self.eval_client.start()

    def stop(self):
        self.dashboard_server.stop()
        self.server.stop()
        self.eval_client.stop()
        self.logout.set()

if __name__ == '__main__':
    ultra96 = ultra96()
    ultra96.start()

    # To prevent it from exiting this thread
    while not ultra96.logout.is_set():
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            ultra96.logout.set()
            ultra96.server.stop()
            ultra96.dashboard_server.stop()
            ultra96.eval_client.stop()