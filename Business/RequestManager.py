from Persistence.DatabaseManager import DatabaseManager
from Business.InventoryManager import InventoryManager
from Business.Request import Request
from Business.Customer import Customer


class RequestManager:
    def __init__(self):
        self.db = DatabaseManager('Requests')

    def addRequest(self, vid, firstName, lastName, email, requestType, requestOpt):
        customer = Customer(firstName,lastName, email)
        inventory = InventoryManager()

        vehicle = inventory.getVehicle(vid)

        if (vehicle['status']):
            request = Request(vehicle['data'], customer, requestType)
            request.addRequestOpt(requestOpt)
            response = self.db.write("", request.toDict() )
        else:
            response  = vehicle

        return response

    def getAllRequests(self):
        response = self.db.getCollection()

        if (not response["status"]):
            response['data'] = []
            return response
        
        data = []
        for doc in response["data"]:
            request = Request(None, None, 1)
            request.toObject(doc.to_dict(), doc.id)
            data.append(request)

        response['data'] = data
        return response

    def getRequest(self, id):
        response = self.db.read(id)

        if (not response["status"]):
            response['data'] = None
            return response

        request = Request(None, None, 1)
        request.toObject(response['data'].to_dict(), response['data'].id)

        response['data'] = request
        return response  


        