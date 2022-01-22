from tkinter import Tk
from tkinter import ttk
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from parse_file import get_values_from_file

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()


def draw_chart(values):
    figure1 = plt.Figure(figsize=(6,5), dpi=100)
    marg = 0.15
    ax = figure1.add_axes([marg, marg, 1-1.8*marg, 1-1.8*marg], aspect=1,
                  )
    ax.plot(values, values, c='C0', lw=2.5, label="Blue signal", zorder=10)
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