from Persistence.DatabaseManager import DatabaseManager
from Business.Vehicle import Vehicle
from firebase_admin import firestore



class InventoryManager:
    def __init__(self, isPublic = False):
        self.db = DatabaseManager('Reliable-Inventory')
        self.isPublic = isPublic
        if (self.isPublic):
            self.addFilter('vehicleStatus','==','Available')

    def addVehicleToInventory(self, chassis, make, model, colour, year, trans, bodyType, mileage, engineNumber, price, priceStatus, location, description):
        vehicle = Vehicle()
        vehicle.newVehicle(chassis, make, model, colour, year, trans, bodyType, mileage, engineNumber, price, priceStatus, location, description)
        return self.db.write(vehicle.id, vehicle)

    def addImagesToVehicle(self, vid, imgSrc, imgDes):
        image = self.db.storeFile(imgSrc, imgDes)
        if (image['status']):
            response = self.db.update(vid, {u'images': firestore.ArrayUnion([u''+ image['data']])})
            return True
        return False

    def resetQuery(self):
        self.db.resetQuery()
        if (self.isPublic):
            self.addFilter('vehicleStatus','==','Available')
        

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
            if (self.isPublic and vehicle.vehicleStatus == "Available"):
                data.append(vehicle)
            elif (not self.isPublic):
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

    def removeVehicle(self, vehicleID):
        return self.db.remove(vehicleID) 

    def updateVehicleField(self, id, field, val):
        return self.db.update(id, {u''+field : u''+val})