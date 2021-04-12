import enum
from datetime import datetime
from .Vehicle import Vehicle
from .Customer import Customer 

import random

def random_char(y):
    alph = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    return ''.join(random.choice(alph) for x in range(y))


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
        self.token = random_char(8) + '-' + random_char(8) + '-' + random_char(8) + '-' + random_char(8) 
        self.tokenValid = True
        self.id = random_char(20)
        self.invoice = ''

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

    def toObject(self, obj):
        self.id = obj['id']
        self.requestType = obj['requestType']
        self.timeStamp = obj['timeStamp']
        self.requestOpt = obj['requestOpt']
        self.token = obj['token']
        self.tokenValid = obj['tokenValid']
        self.invoice = obj['invoice']
        
        self.vehicle = Vehicle()
        self.vehicle.toObject(obj['vehicle'])

        self.customer = Customer('','','')
        self.customer.toObject(obj['customer'])






