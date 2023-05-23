"""
Observer Pattern Classes to Monitor CRUD operations in Database.
"""

from src.config.settings import TEXT_COLOR

# General Subject Class
class Subject:
    observers = []

    def attach(self, obj):
        self.observers.append(obj)
    
    def detach(self, obj):
        pass

    def notify(self, action):
        for observer in self.observers:
            observer.update(action)


# General Observer Class
class Observer():
    def update(self):
        raise NotImplementedError("Delegation to Concrete Observers")

# CRUD Observer Class
class CRUD_Observer(Observer):
    def __init__(self, obj):
        self.observer = obj
        self.observer.attach(self)

    def update(self, action):
        print(TEXT_COLOR['OBSERVER'] + "CRUD Observer Update!" + TEXT_COLOR['END'])
        print(TEXT_COLOR['OBSERVER'] + "Accion Ejecutada: " + action + TEXT_COLOR['END'])
        #print("CRUD Observer Update!")
        #print("Accion Ejecutada:", action)