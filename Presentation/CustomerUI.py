from Business.InventoryManager import InventoryManager
from Persistence.DatabaseManager import DatabaseManager
from Business.Vehicle import Vehicle

class CustomerUI:
    def __init__(self):
        self.inventory = InventoryManager()
    
    def filterInventory(self, make, model, bType, trans, minYear, maxYear):
        self.inventory.resetQuery()

        print(make, model, bType, trans, minYear, maxYear)

        None if make=="" else self.inventory.addFilter("make","==",make)
        None if model=="" else self.inventory.addFilter("model","==",model)
        None if trans=="" else self.inventory.addFilter("trans","==",trans)
        None if bType=="" else self.inventory.addFilter("bodyType","==",bType)

        self.inventory.addFilter("year",">=",minYear)
        self.inventory.addFilter("year","<=",maxYear)
        
        return self.inventory.getQuerriedInventory()
        
    
    def viewVehicle(self, vid):
        return self.inventory.getVehicle(vid)