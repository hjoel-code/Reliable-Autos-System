from Business.InventoryManager import InventoryManager
from Business.RequestManager import RequestManager
from Business.InvoiceManager import InvoiceManager
from Security.Authentication import Authentication
from Persistence.DatabaseManager import DatabaseManager

from random import randint

class UI:
    def __init__(self):
        self.inventory = InventoryManager(True)
        self.request = RequestManager()
    
    def viewInventory(self):
        return self.inventory.getInventory()

    def viewVehicle(self, vid):
        return self.inventory.getVehicle(vid)

    def filterInventory(self, make, model, bType, trans, minYear, maxYear):
        self.inventory.resetQuery()

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
        self.auth  = Authentication()
        self.inventory = InventoryManager()

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
    
    def addInvoice(self, request):
        return self.invoice.addInvoice(request)

    def addInvoiceExpense(self, id, title, expense):
        return self.invoice.addExpensetoInvoice(id, title, expense)

    def addInvoiceDiscount(self, id, title, discount):
        return self.invoice.addDiscounttoInvoice(id, title, discount)

    def generateInvoiceFromRequest(self, request_id):
        response = self.viewRequest(request_id)
        if (response['status']):
            request = response['data']
            if (request.invoice == ''):
                response = self.addInvoice(response['data'])
                if (response['status']):
                    self.inventory.updateVehicleField(request.vehicle.id, 'vehicleStatus', 'Processing')
                    self.request.updateRequestField(request_id, 'invoice', response['data'])
                    response = self.generateInvoice(response['data'])
                    return response
        return response

    def generateInvoice(self, id):
        return self.invoice.getInvoice(id)

    def addCustomerAddress(self, fName, lName, addr1, addr2, addr3, parish, request):
        return self.request.addAddress(fName, lName, addr1, addr2, addr3, parish, request)

    def viewAllInvoices(self):
        return self.invoice.getAllInvoices()

    def addNewAdministrator(self, firstName, lastName, email, password):
        return self.auth.signUpUser(firstName, lastName, email, password)

    def submitVehicleUpdates(self, vid, updates):
        print(updates)
        for key, update in updates.items():
            print(key, update)
            if update != "":
                self.inventory.updateVehicleField(vid, key, update)

