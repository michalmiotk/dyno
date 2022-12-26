import datetime
import os

from isavestate import ISaveState
from memento import Memento 


class SaveState(ISaveState):
    def __init__(self, gui):
        self.gui = gui
        self.figure_filename = ""

    def __call__(self):
        print("I will save")
        now_time = str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
        moto_name = self.gui.get_moto_name()
        self.gui.clear_communicates_label()

        self.figure_filename = "screenshots/" + moto_name + "_" + now_time + ".png"
        self.gui.figure.save_figure(self.figure_filename)

    
    def create_memento(self) -> Memento:
        return Memento(self.figure_filename)

    def restore(self, memento: Memento):
        os.remove(memento.get_chart_filename())