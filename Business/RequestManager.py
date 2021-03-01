from Persistence.DatabaseManager import DatabaseManager
from Business.Request import Request
from Business.Customer import Customer


class RequestManager:
    def __init__(self):
        self.db = DatabaseManager('Requests')

    def addRequest(self, vid, firstName, lastName, email, requestType, requestOpt):
        customer = Customer(firstName,lastName, email)
        request = Request(vid, customer, requestType)
        request.addRequestOpt(requestOpt)
        response = self.db.write("", request.toDict() )
        return response
        


        