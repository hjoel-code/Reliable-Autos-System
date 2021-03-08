from Business.Address import Address

class Customer:
    #Constructor to initialise customer
    def __init__(self, fName, lName, email):
        self.fName = fName
        self.lName = lName
        self.email = email
        self.address = None

    #Setting customer's address
    def setAddress(self, addrLn1, addrLn2, addrLn3, parish):
        self.address = Address(addrLn1, addrLn2, addrLn3, parish)
    
    #Method to return the customer's full name as a string.
    def getFullName(self):
        return self.fName + " " + self.lName

    #Method to return customer's address as a string
    def getAddress(self):
        return self.address.toString()

    #Method to return customer's email as a string
    def getEmail(self):
        return self.email

    def toDict(self):
        try:
            self.address.__dict__
        except:
            pass
        return self

    def toObject(self, obj):
        self.fName = obj['fName']
        self.lName = obj['lName']
        self.email = obj['email']

        try:
            self.address = Address('','','','')
            self.address.toObject(obj['address'])
        except:
            self.address = None