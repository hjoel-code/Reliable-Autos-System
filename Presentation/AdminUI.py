from Persistence.DatabaseManager import DatabaseManager
from Business.Vehicle import Vehicle
from Business.InventoryManager import InventoryManager

import random

class AdminUI:
    def __init__(self):
        self.db = DatabaseManager('Inventory')
        self.inventory = InventoryManager()
        

    def addVehicle(self, chassis, make, model, colour, year, trans, bodyType, mileage, engineNumber, price, priceStatus, location, description):
        newVehicle = Vehicle()
        newVehicle.newVehicle(chassis, make, model, colour, year, trans, bodyType, mileage, engineNumber, price, priceStatus, location, description)
        return self.db.write(newVehicle.id, newVehicle)
        
        # path = "/vehicleImgs/img-"+str(random.randint(1000,9999))+"-"+str(random.randint(1000,9999))
        # url = self.db.storeFile(images, path)
        # self.newVehicle.addImage(url)
        # return None

    def removeVehicle(self, vehicleID):
        return self.db.remove(vehicleID) 

