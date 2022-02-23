from tkinter import Tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import StringVar
from tkinter import OptionMenu
import tkinter
from PIL import ImageTk, Image 

from figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Gui():
    def __init__(self, connect_method, disconnect_method, save_figure_method, select_file_method, get_coms_description_method, print_chart_method):


        self.connect_method = connect_method
        self.disconnect_method = disconnect_method
        self.save_figure_method = save_figure_method
        self.select_file_method = select_file_method
        self.get_coms_description_method = get_coms_description_method
        self.print_chart_method = print_chart_method

        self.question_menu = None
        self.figure = Figure()
        self.root = Tk()
        self.root.title('Dyno')
        photo = tkinter.PhotoImage(file = "logo.png")
        self.root.iconphoto(False, photo)
        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()
        style = ttk.Style(self.root)
        style.theme_use('clam')

        self.figure_column_span = 8

        self.setup_logo(row=0, column=0)
        ttk.Label(self.root, text="Wheel diameter in cm").grid(row=0, column=1)

        self.wheel_diameter_entry = ttk.Entry(self.root)
        self.wheel_diameter_entry.insert(0, '1')
        self.wheel_diameter_entry.grid(row=0, column=2)

        ttk.Label(self.root, text="Entire gear ratio").grid(row=0, column=3)

        self.gear_ratio_entry = ttk.Entry(self.root)
        self.gear_ratio_entry.insert(0, '1')
        self.gear_ratio_entry.grid(row=0, column=4)

        ttk.Label(self.root, text="Moto name").grid(row=0, column=5)

        self.moto_name_entry = ttk.Entry(self.root)
        self.moto_name_entry.grid(row=0, column=6)

        
        
        self.instant_power_label = tkinter.Label(self.root, fg="red", font=("Courier", 24))
        self.instant_power_label.grid(row=2, column=0)
        self.instant_torque_label = tkinter.Label(self.root, fg="blue", font=("Courier", 24))
        self.instant_torque_label.grid(row=2, column=1)

        self.communicates_label = ttk.Label(self.root)
        self.communicates_label.grid(row=2, column=2)

        
        
        ttk.Button(text="Open file", command=self.select_file_method).grid(row=3, column=0)
        ttk.Button(text="Save figure", command=self.save_figure_method).grid(row=3, column=1)
        ttk.Button(text="Print chart", command=self.print_chart_method).grid(row=3, column=2)

        ttk.Button(text="Connect", command=self.connect_method).grid(row=3, column=3)
        self.disconnect_btn = ttk.Button(text="Disconnect", command=self.disconnect_method, state = tkinter.DISABLED)
        self.disconnect_btn.grid(row=3, column=4)
        
        ttk.Button(text="Refresh COMs", command=self.setup_com_dropdown_list).grid(row=3, column=5)
        
        self.setup_com_dropdown_list()

        baud_label = ttk.Label(text="Baud")
        baud_label.grid(row=3, column=7)

        self.baud_entry = ttk.Entry(width=7)
        self.baud_entry.grid(row=3, column=8)
        self.baud_entry.insert(0, '9600')

        self.draw_figure(self.figure.figure)

        
        
        

    def setup_logo(self, row, column):
        logo = Image.open("logo.png")
        logo_small = logo.resize((122, 56), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(logo_small)
        label1 = tkinter.Label(image=test, bg="white")
        label1.image = test
        label1.grid(row=row, column=column)   

    def setup_com_dropdown_list(self):
        self.value_inside = StringVar(self.root)
        port_list = self.get_coms_description_method()
        self.value_inside.set("Select COM")
        if self.question_menu is not None:
            self.question_menu.destroy()
        self.question_menu = OptionMenu(self.root, self.value_inside, *port_list)
        self.question_menu.grid(row=3, column=6)

    def set_instant_power_label(self, instant_power_in_KM: float):
        text = str(round(instant_power_in_KM, 1)) + ' KM'
        self.instant_power_label.config(text=text)    

    def set_instant_torque_label(self, instant_torque_in_Nm: float):
        text = str(round(instant_torque_in_Nm, 1)) + ' Nm'
        self.instant_torque_label.config(text=text)    

    def draw_figure(self, figure):
        canvas = FigureCanvasTkAgg(figure, self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=5, columnspan=self.figure_column_span)

    def draw_internal_figure(self):
        canvas = FigureCanvasTkAgg(self.figure.figure, self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=5, columnspan=self.figure_column_span)

    def get_wheel_diameter(self):
        return float(self.wheel_diameter_entry.get())

    def get_gear_ratio(self):
        return float(self.gear_ratio_entry.get())

    def mainloop(self):
        self.root.mainloop()

    def get_port(self):
        return self.port_entry.get()

    def get_baud(self):
        return self.baud_entry.get()

    def get_moto_name(self):
        return self.moto_name_entry.get()
    
    def set_communicates_label(self, text):
        self.communicates_label.config(text=text)

    def clear_communicates_label(self):
        self.communicates_label.config(text = "")

    def choose_filename(self):
        filetypes = (
            ('text files', '*'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='./',
            filetypes=filetypes)
        
        return filename