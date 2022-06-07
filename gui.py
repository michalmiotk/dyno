from tkinter import Tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import StringVar
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

        self.com_dropdown_list = None
        self.figure = Figure()
        self.root = Tk()
        self.root.title('Dyno')
        photo = tkinter.PhotoImage(file = "imgs/logo.png")
        self.root.iconphoto(False, photo)
        tabControl = ttk.Notebook(self.root)


        self.figure_frm = ttk.Frame(tabControl, padding=10)
        self.figure_frm.grid()
        self.uart_frame = ttk.Frame(tabControl)
        self.uart_frame.grid()
        tabControl.add(self.figure_frm, text ='Figure')
        tabControl.add(self.uart_frame, text ='uart')
        tabControl.pack(expand = 1, fill ="both")



        style = ttk.Style(self.root)
        style.theme_use('clam')
        self.canvas = None
        self.figure_column_span = 8

        self.setup_logo(row=0, column=0)

        self.setup_uart_gui()

        ttk.Label(self.figure_frm, text="Wheel diameter in cm").grid(row=0, column=1)

        self.wheel_diameter_entry = ttk.Entry(self.figure_frm)
        self.wheel_diameter_entry.insert(0, '1')
        self.wheel_diameter_entry.grid(row=0, column=2)

        ttk.Label(self.figure_frm, text="Entire gear ratio").grid(row=0, column=3)

        self.gear_ratio_entry = ttk.Entry(self.figure_frm)
        self.gear_ratio_entry.insert(0, '1')
        self.gear_ratio_entry.grid(row=0, column=4)

        ttk.Label(self.figure_frm, text="Moto name").grid(row=0, column=5)

        self.moto_name_entry = ttk.Entry(self.figure_frm)
        self.moto_name_entry.grid(row=0, column=6)

        self.instant_power_label = tkinter.Label(self.figure_frm, fg="red", font=("Courier", 24))
        self.instant_power_label.grid(row=2, column=0)
        self.instant_torque_label = tkinter.Label(self.figure_frm, fg="blue", font=("Courier", 24))
        self.instant_torque_label.grid(row=2, column=1)

        self.communicates_label = ttk.Label(self.figure_frm)
        self.communicates_label.grid(row=2, column=2)



        ttk.Button(self.figure_frm, text="Open file", command=self.select_file_method).grid(row=3, column=0)
        ttk.Button(self.figure_frm, text="Save figure", command=self.save_figure_method).grid(row=3, column=1)
        ttk.Button(self.figure_frm, text="Print chart", command=self.print_chart_method).grid(row=3, column=2)
        n_rows =1
        n_columns =5
        self.uart_frame.grid_rowconfigure(tuple(range(n_rows+1)),  weight =1)
        self.uart_frame.grid_columnconfigure(tuple(range(n_columns+1)),  weight =1)
        self.canvas = FigureCanvasTkAgg(self.figure.figure, self.figure_frm)
        self.draw_figure()

    def setup_uart_gui(self):
        ttk.Button(self.uart_frame, text="Connect", command=self.connect_method).grid(row=0, column=0, sticky="we")
        self.disconnect_btn = ttk.Button(self.uart_frame, text="Disconnect", command=self.disconnect_method, state = tkinter.DISABLED)
        self.disconnect_btn.grid(row=0, column=1, sticky="we")

        baud_label = ttk.Label(self.uart_frame, text="Baud")
        baud_label.grid(row=0, column=2, sticky="we")
        baud_label.configure(anchor="center")

        self.baud_entry = ttk.Entry(self.uart_frame, justify='center', width=7)
        self.baud_entry.grid(row=0, column=3, sticky="we")
        self.baud_entry.insert(0, '9600')

        ttk.Button(self.uart_frame, text="Refresh COMs", command=self.setup_com_dropdown_list).grid(row=0, column=4)
        self.setup_com_dropdown_list()

    def setup_logo(self, row, column):
        logo = Image.open("imgs/logo.png")
        logo_small = logo.resize((122, 56), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(logo_small)
        label1 = tkinter.Label(self.figure_frm, image=test, bg="white")
        label1.image = test
        label1.grid(row=row, column=column)

    def setup_com_dropdown_list(self):
        self.value_inside = StringVar(self.uart_frame)
        port_list = self.get_coms_description_method()
        self.value_inside.set("Select COM")
        if self.com_dropdown_list is not None:
            self.com_dropdown_list.destroy()
        self.com_dropdown_list = ttk.OptionMenu(self.uart_frame, self.value_inside,*port_list)
        self.com_dropdown_list.grid(row=0, column=5, sticky="we")

    def set_instant_power_label(self, instant_power_in_KM: float):
        text = str(round(instant_power_in_KM, 1)) + ' KM'
        self.instant_power_label.config(text=text)

    def set_instant_torque_label(self, instant_torque_in_Nm: float):
        text = str(round(instant_torque_in_Nm, 1)) + ' Nm'
        self.instant_torque_label.config(text=text)

    def draw_figure(self):

        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=5, columnspan=self.figure_column_span)


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
