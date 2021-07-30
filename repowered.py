import serial
import serial.tools.list_ports

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