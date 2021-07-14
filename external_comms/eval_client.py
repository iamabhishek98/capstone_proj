import socket
from Cryptodome.Cipher import AES
from Cryptodome import Random
import base64
import random
import time
import threading

class Client(threading.Thread):
    def __init__(self, ip_addr, secret_key, ultra96, classifier):
        super(Client, self).__init__()
        self.ultra96 = ultra96
        self.ip_addr = ip_addr
        self.secret_key = secret_key
        self.logout = ultra96.logout
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.classifier = classifier

    # encryption function
    def encrypt_message(self, plain_text):
        plain_text = plain_text.ljust((int(len(plain_text)/AES.block_size) + 1) * AES.block_size," ")
        secret_key = bytes(str(self.secret_key), encoding="utf8")
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        msg = plain_text.encode("utf8")
        encoded = base64.b64encode(iv + cipher.encrypt(msg))
        # pad to buffer size
        encrypted_msg = encoded.ljust(1024, b' ')
        return encrypted_msg

    def send_message(self, msg):
        encrypted_message = self.encrypt_message(msg)
        try:
            self.client.sendall(encrypted_message)
        except:
            print(f"Ultra96 failed to send: {msg}")

    def send_dance_move(self, d1, d2, d3, move, sync_delay):
        eval_message = f"#{d1} {d2} {d3}|{move}|{sync_delay}|"
        print(f"Evaluation Message: {eval_message}")
        self.send_message(eval_message)

    def stop(self):
        self.client.close()
        print(f"Ultra96 client disconnected")

    def receive(self):
        while True:
            msg = str(self.client.recv(1024))
            if msg == str(b''):
                print("LOGOUT!!!!")
                break
            else:
                print(msg)
                self.ultra96.pos = [int(msg[2])-1, int(msg[4])-1, int(msg[6])-1]
                self.classifier.evalServerReplySet(self.ultra96.pos)
            # self.ultra96.reset_data()

    def run(self):
        self.client.connect(self.ip_addr)
        print(f"Ultra96 connected to eval server")
        thread = threading.Thread(target=self.receive)
        thread.start()


class Logout():
    def __init__(self):
        self.logout = "test"

def main():
    logout = Logout()
    client = Client(ip_addr, "9999999999999999", logout)
    client.run()

    ACTIONS = ['gun', 'sidepump', 'hair']
    sync_delays = [1.1, 1.2, 1.3] # havent decided
    pos = [1, 2, 3]
    time.sleep(65)
    while True:
        random.shuffle(ACTIONS)
        random.shuffle(pos)
        random.shuffle(sync_delays)

        client.send_dance_move(pos[0], pos[1], pos[2], ACTIONS[0], sync_delays[0])
        # client.send_dance_move(1, 2, 3, 'gun', 1)
        time.sleep(5)


if __name__ == '__main__':
    main()