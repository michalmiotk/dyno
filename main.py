from tkinter import Tk
from tkinter import ttk
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

def get_values_from_file(filename):
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        values = []
        for row in spamreader:  
            for value in row:
                values.append(int(value))

        return values

def draw_chart(values):
    figure1 = plt.Figure(figsize=(6,5), dpi=100)
    ax1 = figure1.add_subplot(111)
    ax1.plot(values)
    canvas = FigureCanvasTkAgg(figure1, root)
    canvas.draw()
    canvas.get_tk_widget().grid(column=0, row=2, ipadx=40, ipady=20)

def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    values = get_values_from_file(filename)
    draw_chart(values)
    
ttk.Button(frm, text="Otworz plik", command=select_file).grid(column=1, row=1)
root.mainloop()