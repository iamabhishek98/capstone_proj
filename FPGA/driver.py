from pynq import Overlay
import time
import struct

def float_to_decimal(num):
    return int(''.join('{:0>8b}'.format(c) for c in struct.pack('!f', num)),2)

def decimal_to_float(num):
    return struct.unpack('f', struct.pack('I', num))[0]

def decimal_to_binary(num):
    return int(bin(num).replace("0b", ""))


class fpga():
    def __init__(self):
        self.myOverlay = Overlay('/home/xilinx/pynq/overlays/mlp4/mlp4.bit')  
        self.my_ip = self.myOverlay.mlp_0

    def predict(self, data):
        # we expect a flattened list of all the data 600 points
        max_node = -1
        max_node_value = -1

        # print(data)
        # write data to fpga
        my_ip = self.my_ip

        for i in range (0, 39):
            # print(data[i], type(data[i]))
            my_ip.write(0x100 + i*0x4, float_to_decimal(data[i]))

        my_ip.write(0x0, 1)
        # wait abit maybe
        ready_flag = False
        while not ready_flag:
            if my_ip.read(0x0) & 2 != 0:
                ready_flag = True

        # read data from fpga
        result = []
        for i in range (0, 8):
            res = decimal_to_float(my_ip.read(0x200 + i*0x04))
            result.append(res)
            # if max_node_value < result[i]:
            #     max_node_value = result[i]
            #     max_node = i
        # print(result)
        return result

        
            

        
