import datetime
from multiprocessing import Queue
import threading
import serial
from tkinter import Tk
from tkinter import ttk
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from parse_file import get_df_from_file, is_valid_csv
from data_from_df import add_to_df_with_wheel_torque, add_to_df_power_in_KM, add_to_df_engine_rot_speed
from create_figure import Figure
from df_from_uart import df_from_uart_row

import pandas as pd

serial_object = None

root = Tk()
root.title('Hamownia')
frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(root, text="Wheel diameter in cm").grid(row=1, column=0)

wheel_diameter_entry = ttk.Entry(root)
wheel_diameter_entry.insert(0, '1')
wheel_diameter_entry.grid(row=1, column=1)

ttk.Label(root, text="Entire gear ratio").grid(row=2, column=0)

gear_ratio_entry = ttk.Entry(root)
gear_ratio_entry.insert(0, '1')
gear_ratio_entry.grid(row=2, column=1)

ttk.Label(root, text="Moto name").grid(row=3, column=0)

moto_name_entry = ttk.Entry(root)
moto_name_entry.grid(row=3, column=1)

communicates_label = ttk.Label(root)
communicates_label.grid(row=4, column=0)

figure = Figure()
uart_process_queue = Queue()

t1 = None
yar = []

def draw_figure(figure):
    canvas = FigureCanvasTkAgg(figure, root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=5, columnspan=2)

def get_wheel_diameter():
    return float(wheel_diameter_entry.get())

def get_gear_ratio():
    return float(gear_ratio_entry.get())

def is_valid_gear_ratio():
    try:
        get_gear_ratio()
    except ValueError as e:
        print(e)
        print("not valid gear_ratio")
    else:
        return True
    
    return False

def is_valid_wheel_diameter():
    try:
        get_wheel_diameter()
    except ValueError as e:
        print(e)
        print("not valid wheel_diameter")
    else:
        return True
    
    return False


def select_file():
    
    if not is_valid_wheel_diameter():
        communicates_label.config(text = "bad wheel diameter format")
        return

    if not is_valid_gear_ratio():
        communicates_label.config(text = "bad gear ratio format")
        return
    
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    if filename == '':
        communicates_label.config(text = "No choosen file")    
        return
    
    if not is_valid_csv(filename):
        communicates_label.config(text = "No valid csv")    
        return

    communicates_label.config(text = "")  
    df = get_df_from_file(filename)
    add_to_df_with_wheel_torque(df, wheel_diameter_in_cm=get_wheel_diameter())
    add_to_df_power_in_KM(df)
    add_to_df_engine_rot_speed(df, get_wheel_diameter(), get_gear_ratio())
    figure.create_figure(df)
    draw_figure(figure.figure)


def save_figure():
    moto_name = moto_name_entry.get()
    if moto_name == '':
        communicates_label.config(text = "Empty moto name")    
        return
   
    now_time = str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
    if figure.is_figure_empty():
        communicates_label.config(text = "No figure")
        return

    communicates_label.config(text = "") 
    
    figure.save_figure(moto_name + '_' + now_time + '.png')

def get_data(queue, serial_obj):
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
        except TypeError as e:
            print("tajp error", e)
            pass

def update_gui(uart_process_q, df):
    while (1):
        print("update")

        if filter_data:=uart_process_q.get():
            print("plottime", filter_data)
            new_df = df_from_uart_row(filter_data)
            df = pd.concat([df, new_df])
            add_to_df_with_wheel_torque(df, wheel_diameter_in_cm=get_wheel_diameter())
            add_to_df_power_in_KM(df)
            add_to_df_engine_rot_speed(df, get_wheel_diameter(), get_gear_ratio())
            figure.create_figure(df)
            draw_figure(figure.figure)

def connect():
    port = port_entry.get()
    baud = baud_entry.get()

    try:
        serial_object = serial.Serial('COM' + str(port), baud)

    except ValueError:
        print("Enter Baud and Port")
        return

    print("started thread")
    t1 = threading.Thread(target=get_data, args=(uart_process_queue, serial_object))
    t1.daemon = True
    t1.start()


draw_figure(figure.figure)
ttk.Button(frm, text="Open file", command=select_file).grid(row=0, column=0)
ttk.Button(frm, text="Save figure", command=save_figure).grid(row=0, column=1)

ttk.Button(text="Connect", command=connect).grid(row=6, column=0)

baud_label = ttk.Label(text="Baud")
baud_label.grid(row=7, column=0)

baud_entry = ttk.Entry(width=7)
baud_entry.grid(row=7, column=1)
baud_entry.insert(0, '9600')

port_label = ttk.Label(text="Port")
port_label.grid(row=8, column=0)
port_entry = ttk.Entry(width=7)
port_entry.grid(row=8, column=1)
port_entry.insert(0, '1')

df = pd.DataFrame()

t2 = threading.Thread(target=update_gui, args=(uart_process_queue, df))
t2.daemon = True
t2.start()

root.mainloop()