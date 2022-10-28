import serial
import serial.tools.list_ports
import sys
import json
import time
import threading
import queue

def list_comports():
	"""Returns a list of Virtual Com Ports on the system."""
    
	print("Available Serial Devices:")
	ports = serial.tools.list_ports.comports()

	line = 0
	for port in ports:
		print('\t' + str(line) + '\t' + port.device + '\t' + port.hwid)
		line += 1

	print(' ')
	return ports

class ElectronicLoad(serial.Serial):
    def __init__(self, comport):
        super().__init__(comport)
        self.baudrate = 115200
        self.timeout = 0.1
        if not self.is_open:
            self.open()
        
        self.encoding = 'utf-8'

    def get_current(self):
        self.write(":MEAS:CURR?\n".encode(encoding=self.encoding))
        try:
            return float(self.readline().decode(encoding=self.encoding).strip())
        except ValueError:
            print("Could not parse float from response to current query.")
            return 0.0
        except serial.SerialTimeoutException:
            print("Timed out waiting for response.")
            return 0.0

    def get_voltage(self):
        self.write(":MEAS:VOLT?\n".encode(encoding=self.encoding))
        try:
            return float(self.readline().decode(encoding=self.encoding).strip())
        except ValueError:
            print("Could not parse float from response to voltage query.")
            return 0.0
        except serial.SerialTimeoutException:
            print("Timed out waiting for response.")
            return 0.0
    
    def get_resistance(self):
        self.write(":MEAS:RES?\n".encode(encoding=self.encoding))
        try:
            return float(self.readline().decode(encoding=self.encoding).strip())
        except ValueError:
            print("Could not parse float from response to resistance query.")
            return 0.0
        except serial.SerialTimeoutException:
            print("Timed out waiting for response.")
            return 0.0
            
    def get_power(self):
        self.write(":MEAS:POW?\n".encode(encoding=self.encoding))
        try:
            return float(self.readline().decode(encoding=self.encoding).strip())
        except ValueError:
            print("Could not parse float from response to power query.")
            return 0.0
        except serial.SerialTimeoutException:
            print("Timed out waiting for response.")
            return 0.0

    def set_current(self, current):
        self.write(":SOUR:CURR {:.6f}\n".format(current).encode(encoding=self.encoding))


class StdinThread(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q
        self.done = False

    def run(self):
        while not self.done:
            cmd = input()
            obj = json.loads(cmd)
            q.put(obj)


if __name__ == "__main__":
    load = ElectronicLoad(sys.argv[1])
    q = queue.Queue(maxsize=1024)

    stdin_thread = StdinThread(q)
    stdin_thread.start()

    done = False
    while not done:
        while not q.empty():
            try:
                cmd = q.get_nowait()
                load.set_current(cmd['current'])
                q.task_done()
            except KeyError:
                load.set_current(0.0)
        
        rpy_obj = {}
        rpy_obj['voltage'] = load.get_voltage()
        rpy_obj['current'] = load.get_current()
        rpy_obj['resistance'] = load.get_resistance()
        rpy_obj['power'] = load.get_power()
        
        print(json.dumps(rpy_obj))
        sys.stdout.flush()

        time.sleep(0.5)
