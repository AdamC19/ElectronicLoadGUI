from repowered import *
import tkinter as tk
import threading
import time

class ElectronicLoadApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()
        self.done = False
        self.load = None

    def create_widgets(self):
        # SUB-FRAMES
        self.input_frame = tk.Frame(self)
        self.data_frame = tk.Frame(self)
        self.input_frame.grid(row=0, column=0)
        self.data_frame.grid(row=0, column=1)

        # ==== INPUT FRAME ====
        grid_row = 0
        self.refresh_btn = tk.Button(self.input_frame, text="REFRESH", command=self.refresh_comports)
        self.refresh_btn.grid(row=grid_row, column=0)
        self.comport_menubtn = tk.Menubutton(self.input_frame, text="COM0", relief=tk.RAISED)
        self.comport_menubtn.grid(row=grid_row, column=1)

        self.comport_menubtn.menu = tk.Menu(self.comport_menubtn, tearoff=0)
        self.comport_menubtn["menu"] = self.comport_menubtn.menu

        for port in list_comports():
            self.comport_menubtn.menu.add_command(label=port.device, command=lambda: self.update_comport(port.device))

        self.connect_btn = tk.Button(self.input_frame, text="CONNECT", command=self.connect_comport)
        self.connect_btn.grid(row=grid_row, column=2, sticky=tk.W)
        grid_row += 1
        tk.Label(self.input_frame, text="CURRENT: ").grid(row=grid_row, column=0)
        self.current_entry = tk.Entry(self.input_frame)
        self.current_entry.grid(row=grid_row, column=1)
        self.set_current_btn = tk.Button(self.input_frame, text="SET", command=self.set_current)
        self.set_current_btn.grid(row=grid_row, column=2, sticky=tk.W)
        grid_row += 1
        self.reset_current_btn = tk.Button(self.input_frame, text="RESET", command=self.reset_current)
        self.reset_current_btn.grid(row=grid_row, column=2, sticky=tk.W)
        grid_row += 1
        
        # ==== DATA FRAME ====
        grid_row = 0
        tk.Label(self.data_frame, text="Voltage: ").grid(row=grid_row, column=0, sticky=tk.E)
        self.voltage_var = tk.StringVar()
        tk.Label(self.data_frame, textvariable=self.voltage_var).grid(row=grid_row, column=1, sticky=tk.W)
        grid_row += 1
        tk.Label(self.data_frame, text="Current: ").grid(row=grid_row, column=0, sticky=tk.E)
        self.current_var = tk.StringVar()
        tk.Label(self.data_frame, textvariable=self.current_var).grid(row=grid_row, column=1, sticky=tk.W)
        grid_row += 1
        tk.Label(self.data_frame, text="Resistance: ").grid(row=grid_row, column=0, sticky=tk.E)
        self.resistance_var = tk.StringVar()
        tk.Label(self.data_frame, textvariable=self.resistance_var).grid(row=grid_row, column=1, sticky=tk.W)
        grid_row += 1
        tk.Label(self.data_frame, text="Power: ").grid(row=grid_row, column=0, sticky=tk.E)
        self.power_var = tk.StringVar()
        tk.Label(self.data_frame, textvariable=self.power_var).grid(row=grid_row, column=1, sticky=tk.W)
        grid_row += 1

        # ==== QUIT BUTTON ====
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row=1, column=1)
    
    def update_comport(self, value=None):
        print("Update comport {}".format(value))
        self.comport_menubtn['text'] = value

    def refresh_comports(self, value=None):
        print("Refreshing comports: {}".format(value))
        self.comport_menubtn.menu.delete(0, self.comport_menubtn.menu.index(tk.END))
        for port in list_comports():
            self.comport_menubtn.menu.add_command(label=port.device, command=lambda: self.update_comport(port.device))

    def connect_comport(self):
        try:
            self.load = ElectronicLoad(self.comport_menubtn['text'])
        except:
            self.load = None
            print("Could not create the serial port or something")

    def update_load(self):
        if self.load == None:
            return None
        self.voltage_var.set("{:.3f}V".format(self.load.get_voltage()))
        self.current_var.set("{:.3f}A".format(self.load.get_current()))
        self.resistance_var.set("{:.3f}Ohms".format(self.load.get_resistance()))
        self.power_var.set("{:.3f}W".format(self.load.get_power()))
    
    def set_current(self):
        if self.load == None:
            return None
        self.load.set_current(float(self.current_entry.get()))

    def reset_current(self):
        if self.load == None:
            return None
        self.load.set_current(0.0)


def main():
    root = tk.Tk()
    app = ElectronicLoadApp(master=root)

    last_update_time = time.time()
    while not app.done:
        app.update()
        app.update_idletasks()
        if time.time() - last_update_time > 0.5:
            app.update_load()
            last_update_time = time.time()

if __name__ == '__main__':
    main()