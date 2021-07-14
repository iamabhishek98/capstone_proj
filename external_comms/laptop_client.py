import random
import socket
import sshtunnel
from Cryptodome.Cipher import AES
from Cryptodome import Random
import base64
import sys
import time
import threading
import os
import subprocess

SUNFIRE_USER = "chokxy"
SUNFIRE_PASS = ""

# Class for the laptop client, calls the c code and creates an SSH tunnel and handles the connection to the Ultra96
class Client():
    def __init__(self, ip_addr, en_format, dancer_id, secret_key, dancer_name, buff_size=1024):
        self.ip_addr = ip_addr
        self.en_format = en_format

        self.dancer_id = dancer_id
        self.dancer_name = dancer_name
        self.buff_size = buff_size
        self.secret_key = secret_key

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.one_way_trip_delay = 0
        self.server_offset = 0

        self.is_start = threading.Event()
        self.connected = False

    def start_tunnel(self, user, password):
        tunnel1 = sshtunnel.open_tunnel(
            ('sunfire.comp.nus.edu.sg', 22),  # host address for ssh, 22
            # xilinx address to bind to localhost port
            remote_bind_address=('137.132.86.236', 22),
            ssh_username=user,
            ssh_password=password,
            block_on_close=False
        )
        tunnel1.start()
        print('Tunnel into Sunfire opened ' +
              str(tunnel1.local_bind_port))
        tunnel2 = sshtunnel.open_tunnel(
            ssh_address_or_host=(
                'localhost', tunnel1.local_bind_port),
            remote_bind_address=('127.0.0.1', 8081),
            ssh_username='xilinx',
            ssh_password='xilinx',
            local_bind_address=('127.0.0.1', 8081),
            block_on_close=False
        )
        tunnel2.start()
        print('Tunnel into Xilinx opened')
        print('TUNNEL SUCCESS!')

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

    def decrypt_message(self, cipher_text):
        decoded_message = base64.b64decode(cipher_text)
        iv = decoded_message[:16]
        secret_key = bytes(str(self.secret_key), encoding="utf8")
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        decrypted_message = cipher.decrypt(decoded_message[16:]).strip()
        return decrypted_message.decode('utf8')

    # Starts the startup procedure for each laptop
    def procedure(self):
        try:
            self.client.settimeout(2)
            # Send dancer info
            start_msg = f"!S|{self.dancer_id}|{self.dancer_name}|"
            self.send_message(start_msg)

            # # Wait for start
            self.wait_for_start()
            print(f"Server ready to start for dancer {self.dancer_id}")

            self.clock_sync()
            self.is_start.set()
            print(f"Dancer {self.dancer_id} starts......")
        except Exception as e:
            # print("error here")
            print(e)

    def run(self):
        self.start_tunnel(SUNFIRE_USER, SUNFIRE_PASS)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(1)
        self.client.connect(self.ip_addr)
        self.procedure()
        self.connected = True
        print(f"Dancer {self.dancer_id} is connected to Ultra96")

    def send_message(self, msg):
        if self.connected:
            encrypted_message = self.encrypt_message(msg)
            try:
                self.client.sendall(encrypted_message)
                # print(f"Dancer {self.dancer_id} message - {msg}")
            except ConnectionResetError:
                raise ConnectionResetError
            except BrokenPipeError:
                raise ConnectionResetError
       
    # Runs on a separate thread and handles commands from the Ultra96
    def handle_commands(self):
        while True:
            try:
                data = self.client.recv(self.buff_size)
                # curr_time = time.time()
                if data:
                    msg = self.decrypt_message(data)
                    # print(msg)
                    if "!T" in msg:
                        self.clock_sync()
                    elif "!C" in msg:
                        self.stop()
            except socket.timeout:
                pass

    def clock_sync(self):
        t1 = time.time()
        clock_msg = f"!T|{t1}|"
        self.send_message(clock_msg)

        data = self.client.recv(self.buff_size)
        t4 = time.time()
        msg = self.decrypt_message(data)
        split_message = msg.split("|")
        t1 = float(split_message[1])
        t2 = float(split_message[2])
        t3 = float(split_message[3])
        self.one_way_trip_delay = ((t4 - t1) - (t3 - t2)) / 2

        self.send_message(f"O|{self.one_way_trip_delay}|")
        self.server_offset = t4 - t3 - self.one_way_trip_delay
        print(f"Offset calculated: {self.server_offset}")

    # Loops and wait for a start command from the Ultra96
    def wait_for_start(self):
        # Wait for the start packet from server
        isStart = False
        while not isStart:
            try:
                encrypted_msg = self.client.recv(self.buff_size)
                msg = self.decrypt_message(encrypted_msg)
                if "!S" in msg:
                    isStart = True
            except socket.timeout:
                print("Waiting for other dancers to connect!")
            except KeyboardInterrupt:
                self.stop()

    def stop(self):
        close_msg = "!C$"
        self.send_message(close_msg)
        self.client.close()
        print(f"Dancer {self.dancer_id} disconnected")

    # Thread to handle data from the bluno
    def handle_bluno_data(self, data):
        # Don't do anything until start flag is received
        if not self.is_start.is_set():
            print("Evaluation not started")
            return

        try:
            data = data.split("|")[0]
            data = data.split(" ")
            data[12] = str(float(data[12]) / 1000 + self.server_offset)

            formatted_msg = "|".join(data)
            formatted_msg = f"!D|{self.dancer_id}|{formatted_msg}|"
            print(formatted_msg)
            self.send_message(formatted_msg)
        except ConnectionResetError:
            raise ConnectionResetError
    
    # For Week 7 Evaluation
    def dummy_data(self):
        bluno_data = [[random.randint(-10000, 10000) for j in range(12)] for i in range(10)]
        for index, data in enumerate(bluno_data):
            message = "!D|" + f"{self.dancer_id}" + "|"
            for i in data:
                message += (str(i) + "|")
            message += f"{time.time()}|"
            # print(message)
            dancer_client.send_message(message)
            # time.sleep(10)
            if (index + 1) % 40 == 0:
                time.sleep(10)
                dancer_client.send_message("!R")
            time.sleep(0.07)

if __name__ == '__main__':
    HOST_ADDR = ('localhost', 8081)
    EN_FORMAT = "utf-8"
    DANCER_NO = 3
    DANCER_NAME = "XY"
    SECRET_KEY = "9999999999999999"
    BUFF_SIZE = 256

    # create dummy bluno data
    # bluno_data = [[random.randint(-10000, 10000)
    #                for j in range(12)] for i in range(10)]
    # print(bluno_data)
    
    dancer_client = Client(HOST_ADDR, EN_FORMAT, DANCER_NO,
                           SECRET_KEY, DANCER_NAME, BUFF_SIZE)
    dancer_client.run()