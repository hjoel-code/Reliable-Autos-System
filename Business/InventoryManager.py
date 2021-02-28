from Persistence.DatabaseManager import DatabaseManager
from Business.Vehicle import Vehicle

class InventoryManager:
    def __init__(self):
        self.db = DatabaseManager('Inventory')

    def resetQuery(self):
        self.db.resetQuery()

    def addFilter(self, field, operator, value):
        if (value != ""):
            self.db.addQuery(field, operator, value)    
    
    def getQuerriedInventory(self):
        response = self.db.getQuerriedDocs()
        
        if (not response["status"]):
            response['data'] = []
            return response
        
        data = []
        for doc in response["data"]:
            vehicle = Vehicle()
            vehicle.toObject(doc.to_dict())
            data.append(vehicle)
        
        response['data'] = data
        self.resetQuery()
        return response

    def getInventory(self):
        response = self.db.getCollection()

        if (not response["status"]):
            response['data'] = []
            return response
        
        data = []
        for doc in response["data"]:
            vehicle = Vehicle()
            vehicle.toObject(doc.to_dict())
            data.append(vehicle)

        response['data'] = data
        return response

    
    def getVehicle(self, vid):
        response = self.db.read(vid)

        if (not response["status"]):
            response['data'] = None
            return response

        vehicle = Vehicle()
        vehicle.toObject(response['data'].to_dict())

        response['data'] = vehicle
        return response
        


        

