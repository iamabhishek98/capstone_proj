import socket
from Cryptodome.Cipher import AES
from Cryptodome import Random
import base64
import random
import time

class Dashboard_Server():
    def __init__(self, ip_addr, secret_key, dashboard_ready, buff_size=256):

        self.ip_addr = ip_addr
        self.buff_size = buff_size
        self.secret_key = secret_key

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.conn = None
        self.addr = None

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

    def send_message(self, msg):
        encrypted_message = self.encrypt_message(msg)
        try:
            self.conn.sendall(encrypted_message)
        except:
            pass

    # Starts the socket connection for the dashboard server to connect to
    def start(self):
        self.server.bind(self.ip_addr)
        self.server.listen()
        self.server.settimeout(20)
        print("Waiting for dashboard to connect")
        self.conn, self.addr = self.server.accept()            
        print("CONNECTED SERVER")

    def stop(self):
        self.server.close()
        print(f"Socket from ultra96 to dashboard disconnected")

# def main():
#     IP_ADD = ("localhost", 8083)
#     # NO_OF_TIMESTAMP = 5
#     BUFF_SIZE = 256
#     SECRET_KEY = 9999999999999999

#     # server = Dashboard_Server(IP_ADD, SECRET_KEY, dashboard_ready=self.dashboard_ready, BUFF_SIZE)
#     server.start()
#     # for j in range(12):
#     #     server.send_message(f"helloooooo")
#     #     j = j - 1 
#     #     print("SENT!")
#     server.stop()

if __name__ == '__main__':
    main()