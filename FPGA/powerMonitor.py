import pynq
import time

rails = pynq.get_rails()
#print(rails)

if 'VSYS' in rails.keys():
    print("Recordign Ultra96 v1 power...")
    rail_name = 'VSYS'
elif 'PSINT_FP' in rails.keys():
    print("Recording Ultra96 v2 power...")
    rail_name = 'PSINT_FP'
else:
    raise RuntimeError("Cannot determine Ultra96 board version.")
recorder = pynq.DataRecorder(rails[rail_name].voltage, rails[rail_name].current)

recorder.reset()
with recorder.record(0.5):
    time.sleep(5)
    recorder.mark()
    for _ in range (10000000):
        pass
    recorder.mark()
    time.sleep(5)

print(recorder.frame)    

