import socket
import base64
from Cryptodome.Cipher import AES
from Cryptodome import Random
import threading
import sshtunnel
import time
import sys
from db import DB

#import socketio
# Connect to computer localhost which is portforwarded to xilinx localhost
EN_FORMAT = "utf-8"
SECRET_KEY = "9999999999999999"
BUFF_SIZE = 256
SIO_ADDRESS = 'http://localhost:8000'
SUNFIRE_USER = "chokxy"
SUNFIRE_PASS = ""

# Class to receive data from the Ultra96 for the dashboard, runs on the dashboard server
# Sends to socket.io for processing by Ivan
class DashboardClient():
    def __init__(self, ip_addr, secret_key, sio_address, buff_size=256):
        self.ip_addr = ip_addr
        self.buff_size = buff_size
        self.secret_key = secret_key
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sio = socketio.Client()
        self.sio_address = sio_address
        self.shutdown = threading.Event()

    def decrypt_message(self, cipher_text):
        decoded_message = base64.b64decode(cipher_text)
        iv = decoded_message[:16]
        secret_key = bytes(str(self.secret_key), encoding="utf8")
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        decrypted_message = cipher.decrypt(decoded_message[16:]).strip()
        return decrypted_message.decode('utf8')

    # Tunnels into the Ultra96
    def start_tunnel(self, user, password):
        tunnel1 = sshtunnel.open_tunnel(
            ('sunfire.comp.nus.edu.sg', 22), #host address for ssh, 22
            remote_bind_address=('137.132.86.236', 22), #xilinx address to bind to localhost port
            ssh_username=user,
            ssh_password=password,
            block_on_close=False
            )
        tunnel1.start()
        print('[Tunnel Opened] Tunnel into Sunfire opened' + str(tunnel1.local_bind_port))
        tunnel2 = sshtunnel.open_tunnel(
            ssh_address_or_host=('localhost', tunnel1.local_bind_port), #ssh into xilinx
            remote_bind_address=('127.0.0.1', 8083), #binds xilinx host
            ssh_username='xilinx',
            ssh_password='xilinx',
            local_bind_address=('127.0.0.1', 8083), #localhost to bind it to
            block_on_close=False
            )
        tunnel2.start()
        print('[Tunnel Opened] Tunnel into Xilinx opened')

    def recvall(self, conn):
        received_chunks = []
        remaining = self.buff_size
        while remaining > 0:
            received = conn.recv(remaining)
            if not received:
                return None
            received_chunks.append(received)
            remaining -= len(received)
        return b''.join(received_chunks)

    # Listens for data from the Ultra96 and sends to socket.io
    def listening(self):
        # self.client.settimeout(30)
        print("Listening for data")
        db = DB()
        while not self.shutdown.is_set():
            data = self.recvall(self.client)
            # data = self.client.recv(1024)
            if data:
                try:
                    msg = self.decrypt_message(data)
                    msg = msg.strip()
                    print("RECEIVED")
                    print(msg)
                    tokens = msg.split('|')
                    msg_type = tokens[0]

                    if msg_type == '!S':
                        pass
                    elif msg_type == '!D':
                        #msg = "!D|1|0.35000000000000003|-0.037500000000000006|-0.375|3.90625|-126.953125|-39.0625|16171149536416|XY|"
                        [dev, ax, ay, az, gx, gy, gz, time] = list(map(float, tokens[1:9]))
                        db.insertBeetle(int(dev), int(time), ax, ay, az, gx, gy, gz, 1)
                    elif msg_type == '!E':
                        # msg = ""
                        [dev, rms, mav, zcs, time] = list(map(float, tokens[1:6]))
                        db.insertEMG(int(time), rms, mav, zcs)
                    elif msg_type == '!M':
                        # msg = "!M|#3 1 2|sidepump|26 0 45"
                        delays = list(map(int, tokens[3].split(" ")))
                        prediction = tokens[2]
                        db.insertMove(delays[0], delays[1], delays[2], prediction)
                        db.insertPosition(tokens[1][1], tokens[1][3], tokens[1][5])
                    else:
                        pass

                except Exception as e:
                        print("IS IT STUCK HERE")
                        print(e)
                        self.client.close()
                        db.close()
                except ConnectionResetError:
                    print("Connection Reset Error")
                    return
                except KeyboardInterrupt:
                    self.client.close()
                    db.close()
                    sys.exit()

    def run(self):
        self.start_tunnel(SUNFIRE_USER, SUNFIRE_PASS)
        # self.client.connect(self.ip_addr)
        # print(self.sio_address)
        # self.sio.connect(self.sio_address)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ip_addr)
        print(f"[ULTRA96 CONNECTED] Dashboard is connected to Ultra96")
        self.listening()
        self.client.close()
        self.stop()
        print("[CLOSED] Dashboard socket has closed")

    def stop(self):
        self.shutdown.set()

def main():
    HOST_ADDR = ("localhost", 8083)
    BUFF_SIZE = 256
    SECRET_KEY = 9999999999999999
    dashboard_client = DashboardClient(HOST_ADDR, SECRET_KEY, SIO_ADDRESS, BUFF_SIZE)
    dashboard_client.run()

if __name__ == '__main__':
    main()
    