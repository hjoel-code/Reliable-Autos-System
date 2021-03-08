from Business.InventoryManager import InventoryManager
from Business.RequestManager import RequestManager
from Business.InvoiceManager import InvoiceManager
from Security.Authentication import Authentication
from Persistence.DatabaseManager import DatabaseManager

from random import randint

class UI:
    def __init__(self):
        self.inventory = InventoryManager()
        self.request = RequestManager()
    
    def viewInventory(self):
        return self.inventory.getInventory()

    def viewVehicle(self, vid):
        return self.inventory.getVehicle(vid)

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


class CustomerUI(UI):
    def sendRequest(self, vid, firstName, lastName, email, requestType, request):
        response = self.request.addRequest(vid, firstName, lastName, email, requestType, request)
        return response


class AdminUI(UI):
    def __init__(self):
        super().__init__()
        self.auth = Authentication()
        self.invoice = InvoiceManager()

    def addVehicle(self, chassis, make, model, colour, year, trans, bodyType, mileage, engineNumber, price, priceStatus, location, description):
        return self.inventory.addVehicleToInventory(chassis, make, model, colour, year, trans, bodyType, mileage, engineNumber, price, priceStatus, location, description)
        
    def addImages(self, vid, img):
        path = "/vehicleImgs/"+vid+"/img-"+str(randint(1000,9999))+"-"+str(randint(1000,9999))
        return self.inventory.addImagesToVehicle(vid, img, path)
        
    def removeVehicle(self, vehicleID):
        return self.inventory.removeVehicle(vehicleID) 

    def viewAllReaquests(self):
        return self.request.getAllRequests()

    def viewRequest(self, id):
        return self.request.getRequest(id)

    def filterRequest(self):
        pass

    def generateInvoice(self):
        pass

    def addNewAdministrator(self):
        pass


