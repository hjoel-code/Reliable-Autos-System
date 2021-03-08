import enum
from datetime import datetime
from Business.Vehicle import Vehicle
from Business.Customer import Customer 



class RequestType(enum.Enum):
    purchase = 1
    moreinfo = 2
    other = 3

class Request: 
    def __init__(self, vehicle, customer, requestType):
        self.vehicle = vehicle
        self.customer = customer
        self.requestType = RequestType(int(requestType)).__dict__['_name_']
        self.timeStamp = datetime.now()
        self.requestOpt = ""

    def addRequestOpt(self, request):
        self.requestOpt = request

    def getRequestType(self):
        if self.requestType == "purchase":
            return "Vehicle Purchase"
        elif self.requestType == "moreinfo":
            return "More Information"
        else: 
            return "Other"

    def getTimeStamp (self):
        return self.timeStamp

    def toDict(self):
        self.customer = self.customer.toDict().__dict__
        self.vehicle = self.vehicle.__dict__
        return self

    def toObject(self, obj, id):
        self.id = id
        self.requestType = obj['requestType']
        self.timeStamp = obj['timeStamp']
        self.requestOpt = obj['requestOpt']
        
        self.vehicle = Vehicle()
        self.vehicle.toObject(obj['vehicle'])

        self.customer = Customer('','','')
        self.customer.toObject(obj['customer'])






