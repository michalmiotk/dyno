from tkinter import Tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import StringVar
from tkinter import OptionMenu

from figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Gui():
    def __init__(self, connect_method, disconnect_method, save_figure_method, select_file_method, get_coms_description_method):


        self.connect_method = connect_method
        self.disconnect_method = disconnect_method
        self.save_figure_method = save_figure_method
        self.select_file_method = select_file_method
        self.get_coms_description_method = get_coms_description_method
        
        self.figure = Figure()
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
        
        ttk.Button(self.frm, text="Open file", command=self.select_file_method).grid(row=0, column=0)
        ttk.Button(self.frm, text="Save figure", command=self.save_figure_method).grid(row=0, column=1)

        ttk.Button(text="Connect", command=self.connect_method).grid(row=6, column=0)
        ttk.Button(text="Disonnect", command=self.disconnect_method).grid(row=6, column=1)
        
        baud_label = ttk.Label(text="Baud")
        baud_label.grid(row=7, column=0)

        self.baud_entry = ttk.Entry(width=7)
        self.baud_entry.grid(row=7, column=1)
        self.baud_entry.insert(0, '9600')

        self.draw_figure(self.figure.figure)

        self.refresh_coms = ttk.Button(self.frm, text="Open file", command=self.select_file_method).grid(row=0, column=0)

        self.value_inside = StringVar(self.root)
        self.setup_dropdown_list()
        ttk.Button(text="Refresh COMs", command=self.setup_dropdown_list).grid(row=8, column=1)
    def setup_dropdown_list(self):
        print("setupuje dropdown")
        port_list = self.get_coms_description_method()
        self.value_inside.set("Select COM")
        self.question_menu = OptionMenu(self.root, self.value_inside, *port_list)
        self.question_menu.grid(row=8, column=0)
    

    def draw_figure(self, figure):
        canvas = FigureCanvasTkAgg(figure, self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=5, columnspan=2)

    def draw_internal_figure(self):
        canvas = FigureCanvasTkAgg(self.figure.figure, self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=5, columnspan=2)

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