import datetime
import queue
import threading

import serial
from tkinter import Tk
from tkinter import ttk
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

from parse_file import get_df_from_file, is_valid_csv
from data_from_df import add_to_df_with_wheel_torque, add_to_df_power_in_KM, add_to_df_engine_rot_speed
from figure import Figure
from df_from_uart import df_from_uart_row



class Program():
    def __init__(self):

        self.serial_object = None

        self.root = Tk()
        self.root.title('Hamownia')
        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()

        ttk.Label(self.root, text="Wheel diameter in cm").grid(row=1, column=0)

        self.wheel_diameter_entry = ttk.Entry(self.root)
        self.wheel_diameter_entry.insert(0, '1')
        self.wheel_diameter_entry.grid(row=1, column=1)

        ttk.Label(self.root, text="Entire gear ratio").grid(row=2, column=0)

        self.gear_ratio_entry = ttk.Entry(self.root)
        self.gear_ratio_entry.insert(0, '1')
        self.gear_ratio_entry.grid(row=2, column=1)

        ttk.Label(self.root, text="Moto name").grid(row=3, column=0)

        self.moto_name_entry = ttk.Entry(self.root)
        self.moto_name_entry.grid(row=3, column=1)

        self.communicates_label = ttk.Label(self.root)
        self.communicates_label.grid(row=4, column=0)

        self.figure = Figure()
        self.uart_process_queue = queue.Queue()

        self.update_gui_enabled = False
        self.uart_df = pd.DataFrame()
        self.serial_object = None

        self.draw_figure(self.figure.figure)

        ttk.Button(self.frm, text="Open file", command=self.select_file).grid(row=0, column=0)
        ttk.Button(self.frm, text="Save figure", command=self.save_figure).grid(row=0, column=1)

        ttk.Button(text="Connect", command=self.connect).grid(row=6, column=0)
        ttk.Button(text="Disonnect", command=self.disconnect).grid(row=6, column=1)
        baud_label = ttk.Label(text="Baud")
        baud_label.grid(row=7, column=0)

        self.baud_entry = ttk.Entry(width=7)
        self.baud_entry.grid(row=7, column=1)
        self.baud_entry.insert(0, '9600')

        port_label = ttk.Label(text="Port")
        port_label.grid(row=8, column=0)
        self.port_entry = ttk.Entry(width=7)
        self.port_entry.grid(row=8, column=1)
        self.port_entry.insert(0, '1')
        
        self.root.mainloop()

    def draw_figure(self, figure):
        canvas = FigureCanvasTkAgg(figure, self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=5, columnspan=2)

    def get_wheel_diameter(self):
        return float(self.wheel_diameter_entry.get())

    def get_gear_ratio(self):
        return float(self.gear_ratio_entry.get())

    def is_valid_gear_ratio(self):
        try:
            self.get_gear_ratio()
        except ValueError as e:
            print(e)
            print("not valid gear_ratio")
        else:
            return True
    
        return False

    def is_valid_wheel_diameter(self):
        try:
            self.get_wheel_diameter()
        except ValueError as e:
            print(e)
            print("not valid wheel_diameter")
        else:
            return True
        
        return False


    def select_file(self):
        
        if not self.is_valid_wheel_diameter():
            self.communicates_label.config(text = "bad wheel diameter format")
            return

        if not self.is_valid_gear_ratio():
            self.communicates_label.config(text = "bad gear ratio format")
            return
    
        filetypes = (
            ('text files', '*'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='./',
            filetypes=filetypes)

        if filename == '':
            self.communicates_label.config(text = "No choosen file")    
            return
        
        if not is_valid_csv(filename):
            self.communicates_label.config(text = "No valid csv")    
            return

        self.communicates_label.config(text = "")  
        df = get_df_from_file(filename)
        add_to_df_with_wheel_torque(df, wheel_diameter_in_cm=self.get_wheel_diameter())
        add_to_df_power_in_KM(df)
        add_to_df_engine_rot_speed(df, self.get_wheel_diameter(), self.get_gear_ratio())
        self.figure.update_figure(df)
        self.draw_figure(self.figure.figure)


    def save_figure(self):
        moto_name = self.moto_name_entry.get()
        if moto_name == '':
            self.communicates_label.config(text = "Empty moto name")    
            return
    
        now_time = str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
        if self.figure.is_figure_empty():
            self.communicates_label.config(text = "No figure")
            return

        self.communicates_label.config(text = "") 
    
        self.figure.save_figure(moto_name + '_' + now_time + '.png')

    def get_data(self, queue, serial_obj):
        while serial_obj.isOpen():
            print("begin of reading from serial")
            try:
                serial_data = serial_obj.readline()
                serial_data = serial_data.decode("UTF-8")
                print("oooo", serial_data)
                serial_data = serial_data.strip('\n').strip('\r')
                print(serial_data)
                filter_data = serial_data.split(',')
                filter_data = [int(d) for d in filter_data]
                queue.put(filter_data)
                print("dane wsadzone")
            except TypeError as e:
                print("tajp error", e)
                pass

    def update_gui(self, uart_process_q):
        while (self.update_gui_enabled):
            print("update")
            try:
                print("probouje zdobyc dane")
                filter_data =uart_process_q.get()
                print("plottime", filter_data)
                new_df = df_from_uart_row(filter_data)
                self.uart_df = pd.concat([self.uart_df, new_df])
                add_to_df_with_wheel_torque(self.uart_df, wheel_diameter_in_cm=self.get_wheel_diameter())
                add_to_df_power_in_KM(self.uart_df)
                add_to_df_engine_rot_speed(self.uart_df, self.get_wheel_diameter(), self.get_gear_ratio())
                self.figure.update_figure(self.uart_df)
                self.draw_figure(self.figure.figure)
            except queue.Empty as e:
                print(e)
        print("updating gui stopped")

    def start_update_gui_thread(self):
        t2 = threading.Thread(target=self.update_gui, args=(self.uart_process_queue,))
        t2.daemon = True
        t2.start()

    def connect(self):
        self.uart_df = pd.DataFrame()
        port = self.port_entry.get()
        baud = self.baud_entry.get()
        try:
            self.serial_object = serial.Serial('COM' + str(port), baud)

        except ValueError:
            print("Enter Baud and Port")
            return

        print("started thread")
        t1 = threading.Thread(target=self.get_data, args=(self.uart_process_queue, self.serial_object))
        t1.daemon = True
        t1.start()
        self.update_gui_enabled = True
        self.start_update_gui_thread()

    def disconnect(self):
        if self.serial_object is not None:
            self.uart_df = pd.DataFrame()
            self.serial_object.close()
            self.update_gui_enabled = False

if __name__ == '__main__':
    program = Program()