from pynq import DefaultIP

class AddDriver(DefaultIP):
    def __init__(self, description:
        super().__init__(description=description)

        bindto = ['xilinx.com:hls:mlp:1.0']

        def input(self, a, b, c, d, e, f, g):
            input_start = 0x10
            size = 0x04
            self.write(input_start, a)
            self.write(input_start + size, b)
            self.write(input_start + 2*size, c)
            self.write(input_start + 3*size, d)
            self.write(input_start + 4*size, e)
            self.write(input_start + 5*size, f)
            self.write(input_start + 6*size, g)
            return self.read(0x40)