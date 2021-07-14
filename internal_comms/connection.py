from bluepy import btle
from bluepy.btle import Peripheral,Scanner,DefaultDelegate,UUID,BTLEDisconnectError,BTLEException
from datetime import datetime
from copy import deepcopy
from time import time, sleep
from math import ceil
import os
import threading
import sys
import csv
import base64
import socket
import struct
import random

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from external_comms.laptop_client import Client

INTERVAL = 60
ERROR_THRESHOLD = 10
ACTUAL_DATA_STATUS = True
start = 0

service_id = "0000dfb0-0000-1000-8000-00805f9b34fb"
BEETLE_1 = "80:30:dc:d9:1c:74"
BEETLE_2 = "34:b1:f7:d2:35:81"
BEETLE_3 = "80:30:dc:d9:1c:17"
BEETLE_4 = "80:30:dc:d9:0c:d2"
BEETLE_5 = "80:30:dc:d9:0c:a1"
BEETLE_6 = "80:30:dc:d9:1c:3f"

addr_arr = [ BEETLE_1, BEETLE_2, BEETLE_3,BEETLE_4,BEETLE_5,BEETLE_6]

addr_map = {}
addr_map[BEETLE_1] = 1
addr_map[BEETLE_2] = 2
addr_map[BEETLE_3] = 3
addr_map[BEETLE_4] = 4
addr_map[BEETLE_5] = 5
addr_map[BEETLE_6] = 6

handshake_status_map = {}
handshake_status_map[BEETLE_1] = False
handshake_status_map[BEETLE_2] = False
handshake_status_map[BEETLE_3] = False
handshake_status_map[BEETLE_4] = False
handshake_status_map[BEETLE_5] = False
handshake_status_map[BEETLE_6] = False

reset_status_map = deepcopy(handshake_status_map)

reset_count_map = {}
reset_count_map[BEETLE_1] = 0
reset_count_map[BEETLE_2] = 0
reset_count_map[BEETLE_3] = 0
reset_count_map[BEETLE_4] = 0
reset_count_map[BEETLE_5] = 0
reset_count_map[BEETLE_6] = 0

total_count_map = deepcopy(reset_count_map)
error_total_count_map = deepcopy(reset_count_map)
error_current_count_map = deepcopy(reset_count_map)
error_other_count_map = deepcopy(reset_count_map)
clock_sync_map = deepcopy(reset_count_map)

# Packet codes
HANDSHAKE = 'H'
ACK = 'A'
DATA = 'D'
RESET = 'R'
DELIMITER = '|'

HOST_ADDR = ('localhost', 8081)
EN_FORMAT = "utf-8"
DANCER_NAME = "XY"
SECRET_KEY = "9999999999999999"
BUFF_SIZE = 256


if ACTUAL_DATA_STATUS:
	# 5 to be removed
	dance_client = Client(HOST_ADDR, EN_FORMAT, 5, SECRET_KEY, DANCER_NAME, BUFF_SIZE)
	dance_client.run()

def printStats(addr):
	print('\n<----------------------------------- BEETLE %s STATS ----------------------------------->'%addr_map[addr])
	print('Time elapsed: %s seconds'%str(INTERVAL))
	print('Total packets successfully received:',total_count_map[addr])
	print('Total packets dropped due to bad checksum:',error_total_count_map[addr]-error_other_count_map[addr])
	print('Total packets dropped due to other reasons:',error_other_count_map[addr])
	print('Total number of reset times:',reset_count_map[addr])
	print('Data rate: %s Hz'%str(ceil(total_count_map[addr]/INTERVAL)))
	print('Success rate:', round((total_count_map[addr]-error_total_count_map[addr])/total_count_map[addr]*100,2),'%\n')

def main():
	global start
	devices = Setup.scanDevices()

	for d in devices:	
		if d.addr in addr_arr:
			start = time()
			print("Connecting to Beetle %s..." % (addr_map[d.addr]))
			beetle = Setup.formPeripheral(d.addr)
			print("Successfully formed peripheral with Beetle %s!" %(addr_map[d.addr]))
			CommsThread(beetle).start()
class Setup:
	def scanDevices():
		scanner = Scanner(0)
		print("Scanning...")
		devices = scanner.scan(5) # increase number to increase scanning duration
		beetle_count = 0
		for i in devices:
			if i.addr in addr_arr: beetle_count += 1
		print(str(beetle_count)+' Beetle(s) Found!')
		return devices

	def formPeripheral(addr):
		try:	
			beetle = Peripheral(addr,btle.ADDR_TYPE_PUBLIC,0)
		except:
			print("Error! Attempting to reform peripheral with Beetle %s..."%addr_map[addr])
			sleep(1)
			beetle = Setup.formPeripheral(addr)
		return beetle
class Delegate(btle.DefaultDelegate):
	global handshake_status_map
	global reset_status_map
	global total_count_map
	global error_current_count_map
	global error_total_count_map
	global error_other_count_map
	global dance_client

	def __init__(self,addr):
		btle.DefaultDelegate.__init__(self)
		self.addr = addr
		self.packet = ""
		self.buffer = b''
		DANCER_NO = addr_map[self.addr]
		if ACTUAL_DATA_STATUS: self.client = dance_client

	def handleNotification(self,cHandle,fragment):
		if (time() > start + INTERVAL): 
			printStats(self.addr)
			sys.exit()

		if handshake_status_map[self.addr]:
			self.buffer += fragment
			if len(fragment)>=11:
				current = self.buffer[0:11]
				self.processData(current)

				self.buffer = self.buffer[11:]
		elif len(fragment) == 1:
			packet_code = struct.unpack('!c',fragment)[0]
			if packet_code == b'A':
				clock_sync_map[self.addr] = round(time()*1000)
				handshake_status_map[self.addr] = True
				print('ACK packet received from Beetle %s'%addr_map[self.addr])
				
	def processData(self, data):
		if data[0] == 68:
			b = struct.unpack('!cbbbbbbLb', data)
			if checkChkSum(b):
				for i, x in enumerate(b):
					if i == len(b) - 2:
						x = clock_sync_map[self.addr] + x
					if isinstance(x, bytes):
						x = x.decode('utf-8') + "|" + str(addr_map[self.addr])
					self.packet += str(x) + "|"
				self.sendData()
				self.packet = ""
	
	def sendData(self):
		if ACTUAL_DATA_STATUS: 
			self.client.send_message(self.packet)
		else:
			print('DATA from Beetle %s:'%addr_map[self.addr],self.packet)
		
	def checkChkSum(self, data):
		try:
			received_chksum = data[-1]
			data = data[0:len(data)-1]
			chksum = 0
			for i in range(len(data)):
				chksum ^= ord(data[i])
			if (chksum != received_chksum): return False
			return True
		except ValueError:
			return False
		except Exception as e:
			print(self.packet)
			print(e)
			error_other_count_map[self.addr] += 1
			return False

class CommsThread(threading.Thread):
	global reset_status_map
	global reset_count_map

	def __init__(self,beetle):
		threading.Thread.__init__(self)
		self.beetle = beetle
		self.serial_service = beetle.getServiceByUUID(service_id)
		self.serial_char = self.serial_service.getCharacteristics()[0] 
			
	
	def run(self):
		try:
			self.beetle.setDelegate(Delegate(self.beetle.addr))
			if (self.initHandshake()):
				while True:
					if self.beetle.waitForNotifications((2.0)) and not reset_status_map[self.beetle.addr]:
						continue
					
					if (reset_status_map[self.beetle.addr]): break
				print('Error! Too many corrupted packets detected! Resetting Beetle %s...'%addr_map[self.beetle.addr])
				self.serial_char.write(bytes(RESET,'utf-8'),withResponse = False)
				reset_count_map[self.beetle.addr] += 1
				reset_status_map[self.beetle.addr] = False
				handshake_status_map[self.beetle.addr] = False
				self.beetle.disconnect()
				self.reconnect()
			else:
				print('Handshake Failure with Beetle %s!'%addr_map[self.beetle.addr])
				handshake_status_map[self.beetle.addr] = False
				self.beetle.disconnect()
				self.reconnect()
		
		except BTLEDisconnectError:
			handshake_status_map[self.beetle.addr] = False
			print('Error! Beetle %s got disconnected!'%addr_map[self.beetle.addr])
			self.reconnect()
	
	def reconnect(self):
		sleep(5)
		print('Attempting to reconnect with Beetle %s...'%addr_map[self.beetle.addr])
		try:
			self.beetle.connect(self.beetle.addr)
			sleep(3)
			print('Reconnected to Beetle %s'%addr_map[self.beetle.addr])
			self.run()
		except Exception as e:
			print(e)
			print('Error! Unable to connect to Beetle %s'%addr_map[self.beetle.addr])
			self.reconnect()

	def initHandshake(self):
		print('Initializing handshake with Beetle %s...'%addr_map[self.beetle.addr])
		
		# reset beetle before connecting to it
		self.serial_char.write(bytes(RESET,'utf-8'),withResponse = False)
		sleep(1)

		count = 1
		while not handshake_status_map[self.beetle.addr]:
			self.serial_char.write(bytes(HANDSHAKE,'utf-8'),withResponse = False)
			print(str(count) + " HANDSHAKE packet(s) sent to Beetle %s"% addr_map[self.beetle.addr])
			
			if self.beetle.waitForNotifications(2.0):
				print("Successfully connected to Beetle %s!" % (addr_map[self.beetle.addr]))
				self.serial_char.write(bytes(ACK,'utf-8'),withResponse = False)
				return True
			
			count += 1
		
if __name__ == '__main__':
	main()