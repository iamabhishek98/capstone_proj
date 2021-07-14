import socket
import threading
import time
import base64
from Cryptodome.Cipher import AES
import sys
from Cryptodome import Random
import time as time2
from statistics import mean
import os
import traceback

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
# from Test.runLivePrediction_ultra96 import classificationEngine
from Test.relayMain import classificationEngine

# Class to handle the connection to the laptop (acts as the server and opens the socket)
class Server(threading.Thread):
    def __init__(self, ip_addr, secret_key, ultra96, sync_threshold, buff_size, dancers_count):
        super(Server, self).__init__()

        self.ip_addr = ip_addr
        self.buff_size = buff_size
        self.dancers_count = dancers_count
        self.secret_key = secret_key
        self.ultra96 = ultra96
        self.logout = ultra96.logout
        self.dancers_ready = ultra96.dancers_ready
        self.sync_threshold = sync_threshold
        self.first_x_timestamp = {}
        self.dancer_data = {}
        self.classifier = classificationEngine(self.sendClassificationToDashboard)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_connection = []

    def sendClassificationToDashboard(self, position, predictedResult, syncDelay, formattedEVALSyncDelay):
        dashboard_msg = "!M|{pos}|{prediction}|{syncdelay}".format(pos = position, prediction=predictedResult, syncdelay = syncDelay)
        print(dashboard_msg)
        self.ultra96.dashboard_server.send_message(dashboard_msg)
        eval_msg = "{pos}|{prediction}|{syncdelay}".format(pos = position, prediction = predictedResult, syncdelay=formattedEVALSyncDelay)
        print(eval_msg)
        self.ultra96.eval_client.send_message(eval_msg)
            
    def stop(self):
        for conn in self.socket_connection:
            conn.close()
        self.socket.close()
        print("Ultra96 Server Has Closed")

    def recvall(self, conn):
        # Buffer to ensure that only reading the full 256 bytes
        received_chunks = []
        remaining = self.buff_size
        while remaining > 0:
            received = conn.recv(remaining)
            if not received:
                return None
            received_chunks.append(received)
            remaining -= len(received)
        return b''.join(received_chunks)

    # Function to handle the messages from each socket, runs on a separate thread
    def handle_client(self, conn, addr):
        self.dancers_count -= 1
        dancer_id = -1
        dancer_name = ""
        network_delay = 0
        time = time2
        while True:
            data = self.recvall(conn)
            recv_time = time.time()
            # recv_time = 0
            if data:
                try:
                    msg = self.decrypt_message(data)
                    msg = msg.strip()
                    # Calculate clock offset (Week 7 Evaluation)
                    if "!T" in msg:
                        self.clock_sync(conn, msg, dancer_id, recv_time)
                    
                    elif "!S" in msg:
                        # Start message
                        split_message = msg.split("|")
                        dancer_id = int(split_message[1])
                        dancer_name = str(split_message[2])
                        time.sleep(0.02 * int(dancer_id))
                        self.ultra96.dashboard_server.send_message(msg)
                        self.create_dancer(dancer_id, dancer_name)
                        print(
                            # f"Dancer {dancer_id} {dancer_name} connected.")
                            f"Server received start packet from dancer {dancer_id}.")  
                    
                    # Dancers sensor data
                    elif "!D" in msg:
                        # Data message
                        dashboard_message = msg + f"{dancer_name}|"
                        self.ultra96.dashboard_server.send_message(
                            dashboard_message)
                        tokens = msg.split("|")
                        [dev, ax, ay, az, gx, gy, gz, ts] = list(map(float, tokens[1:9]))
                        self.classifier.add_data("DATA", [dev, ax, ay, az, gx, gy, gz])
                    
                    # Calculate network delay (Week 7 Evaluation)
                    elif "O" in msg:
                        network_delay = float(msg.split("|")[1])
                        print(network_delay)
                    
                    # EMG Data
                    elif "!E" in msg:
                        dashboard_message = msg
                        self.ultra96.dashboard_server.send_message(
                            dashboard_message)
                        tokens = msg.split("|")
                        [dev, gx, gy, gz, ts] = list(map(float, tokens[1:6]))
                        self.classifier.add_data("EMG", [ gx, gy, gz])
                
                except Exception as e:
                    traceback.print_exc()
                    print(e)
            else:
                # print(f"Calculated sync delay is: {self.sync_delay}")
                print(f"No more data received from {dancer_id}")
                break
        print(
            f"Dancer {dancer_id} has disconnected")

    def start_clock_sync_all(self):
        for conn in self.socket_connection:
            self.send_message(conn, "!T|")

    # Replies the clock synchronisation protocol
    def clock_sync(self, conn, msg, dancer_id, recv_time):
        msg += f"{recv_time}|"
        send_time = time.time()
        msg += f"{send_time}|"
        self.send_message(conn, msg, dancer_id=dancer_id)

    def create_dancer(self, dancer_id, dancer_name):
        self.dancer_data[dancer_id - 1] = []
        # self.dancer_names[dancer_id - 1] = dancer_name
        self.first_x_timestamp[dancer_id - 1] = []

    def add_data(self, dancer_id, data):
        if len(self.first_x_timestamp[dancer_id - 1]) < 7:
            data[8] = float(data[8])
            self.first_x_timestamp[dancer_id - 1].append(data[8])
            print(f"{len(self.first_x_timestamp[dancer_id - 1])} timestamp(s) of dancer " 
                + f"{dancer_id}" + " collected.")
        
        if (len(self.first_x_timestamp[0]) == 7) and (len(self.first_x_timestamp[1]) == 7) and (len(self.first_x_timestamp[2]) == 7):
            self.get_sync_delay()
            self.first_x_timestamp[dancer_id - 1] = []
        
        # else:
        #     self.first_x_timestamp[dancer_id - 1] = []
    
    # Calculate Sync Delay (for Week 7 evaluation)
    def get_sync_delay(self):
        start_of_each_dancer = [mean(timestamps)
                                for timestamps in self.first_x_timestamp.values()]
        earliest_dancer = min(start_of_each_dancer)
        latest_dancer = max(start_of_each_dancer)
        self.sync_delay = int((latest_dancer - earliest_dancer) * 1000)
        print(f"Calculated sync delay is: {self.sync_delay}")

    def run(self):
        self.socket.bind(self.ip_addr)
        self.socket.listen()
        self.socket.settimeout(5)
        print(
            f"Waiting for {self.dancers_count} connection(s)")
        while self.dancers_count > 0:
            try:
                conn, addr = self.socket.accept()
                thread = threading.Thread(
                    target=self.handle_client, args=(conn, addr))
                self.socket_connection.append(conn)
                thread.start()
            except socket.timeout:
                pass
            except OSError:
                pass
            print(f"{len(self.socket_connection)} dancers connected.")
            self.dancers_ready.set()

    # Sends a start message to all dancers
    def start_evaluation(self):
        # Start command
        for idx, conn in enumerate(self.socket_connection):
            self.send_message(conn, "!S")
            conn_idx = idx + 1
            print(f"Server sends start packet to connection {conn_idx}")
        for dancer in self.first_x_timestamp.keys():
            self.first_x_timestamp[dancer] = []

    def send_message(self, conn, msg, dancer_id="ALL"):
        encrypted_message = self.encrypt_message(msg)
        try:
            conn.sendall(encrypted_message)
        except:
            pass

    def decrypt_message(self, cipher_text):
        decoded_message = base64.b64decode(cipher_text)
        iv = decoded_message[:16]
        secret_key = bytes(str(self.secret_key), encoding="utf8")
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        decrypted_message = cipher.decrypt(decoded_message[16:]).strip()
        return decrypted_message.decode('utf8')

    def encrypt_message(self, plain_text):
        plain_text = plain_text.ljust((int(len(plain_text)/AES.block_size) + 1) * AES.block_size," ")
        secret_key = bytes(str(self.secret_key), encoding="utf8")
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        msg = plain_text.encode("utf8")
        encoded = base64.b64encode(iv + cipher.encrypt(msg))
        # pad to buffer size
        encrypted_msg = encoded.ljust(self.buff_size, b' ')
        return encrypted_msg

class Logout():
    def __init__(self):
        self.logout = "test"

def main():
    ULTRA_SERVER_ADDR = ('localhost', 8081)
    NUM_OF_DANCERS = 1
    SYNC_THRESHOLD = 0.2
    # NO_OF_TIMESTAMP = 5
    BUFF_SIZE = 256
    SECRET_KEY = 9999999999999999
    logout = Logout()

    server = Server(ULTRA_SERVER_ADDR, SECRET_KEY, logout, SYNC_THRESHOLD, BUFF_SIZE, NUM_OF_DANCERS)
    server.run()
    server.start_evaluation()

if __name__ == '__main__':
    main()