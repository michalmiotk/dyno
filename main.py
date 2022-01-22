from tkinter import Tk
from tkinter import ttk
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from parse_file import get_df_from_file, is_valid_csv
from data_from_df import add_to_df_with_wheel_torque, add_to_df_power_in_KM, add_to_df_engine_rot_speed
from create_figure import create_figure


root = Tk()
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

communicates_label = ttk.Label(root)
communicates_label.grid(row=3, column=0)



def draw_chart(df):
    figure = create_figure(df)
    canvas = FigureCanvasTkAgg(figure, root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=4, column=0, ipadx=40, ipady=20)



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
    df_with_wheel_torque = add_to_df_with_wheel_torque(df, wheel_diameter_in_cm=get_wheel_diameter())
    df_with_wheel_torque_and_power_in_KM = add_to_df_power_in_KM(df)
    df_with_wheel_torque_and_power_in_KM_and_engine_rot_speed = add_to_df_engine_rot_speed(df, get_wheel_diameter(), get_gear_ratio())
    draw_chart(df_with_wheel_torque_and_power_in_KM_and_engine_rot_speed)
    
ttk.Button(frm, text="Otworz plik", command=select_file).grid(column=1, row=1)
root.mainloop()