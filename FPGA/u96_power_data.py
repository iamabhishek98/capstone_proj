import pynq
import time

rails = pynq.get_rails()

#Power rail for FPGA power
rail_name_FPGA = 'PSPLL'
#Power rail for CPU power
rail_name_CPU = "PSINT_FP"

#create Pynq Datarecorder to record power
recorder_FPGA = pynq.DataRecorder(rails[rail_name_FPGA].power)
recorder_CPU = pynq.DataRecorder(rails[rail_name_CPU].power)

recording_interval = 120 # Record power every 120 seconds (2 minutes)

#record powers for FPGA and CPU
recorder_FPGA.record(recording_interval)
recorder_CPU.record(recording_interval)

System_run_time = 30*60 # 30 minutes system run time
time.sleep(System_run_time) # The code waits for 30 minutes during your system evaluation of 30 minutes

#save to csv file
recorder_FPGA.frame.to_csv('FPGA_power.csv')
recorder_CPU.frame.to_csv('CPU_power.csv')
