from isavestate import ISaveState
from memento import Memento


class SaveStateEmptyFigure(ISaveState):
    def __init__(self, gui):
        self.gui = gui

    def __call__(self):
        print("no figure")
        self.gui.set_communicates_label("No figure")

    def create_memento(self) -> Memento:
        return None

    def restore(self, memento: Memento):
        pass