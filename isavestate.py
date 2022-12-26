from memento import Memento

class ISaveState:
    def __init__(self, arg):
        pass
    
    def __call__(self):
        raise NotImplementedError

    def create_memento(self) -> Memento:
        raise NotImplementedError

    def restore(self, memento: Memento):
        raise NotImplementedError