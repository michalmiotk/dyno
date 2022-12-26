from memento import Memento
from isavestate import ISaveState

class SaveStateMissingField(ISaveState):
    def __init__(self, gui):
        self.gui = gui

    def __call__(self):
        self.gui.set_communicates_label("Empty moto name")

    def create_memento(self) -> Memento:
        return None

    def restore(self, memento: Memento):
        pass
