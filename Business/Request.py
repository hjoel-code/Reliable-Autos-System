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
        return self.RequestType

    def getTimeStamp (self,timeStamp):
        return self.timestamp

    def toDict(self):
        self.customer = self.customer.toDict().__dict__

        return self





