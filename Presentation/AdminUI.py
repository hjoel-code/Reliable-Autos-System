from Persistence.DatabaseManager import DatabaseManager
from Business.Vehicle import Vehicle
from Business.InventoryManager import InventoryManager

class AdminUI:
    def __init__(self):
        self.db = DatabaseManager('Inventory')
        self.inventory = InventoryManager()

    def addVehicle(self, chassis, make, model, year, price, colour, trans, bodyType, mileage, engineNumber, ccRating):
        newVehicle = Vehicle(chassis)
        newVehicle.setAttr(make,model,colour,year,trans,bodyType,mileage,engineNumber,ccRating,price)
        return self.db.write(newVehicle, newVehicle.getID())

    def removeVehicle(self, vehicleID):
        return self.db.remove(vehicleID) 

