from Business.Address import Address

class Customer:
    def __init__(self, fName, lName, email):
        self.fName = fName
        self.lName = lName
        self.email = email

    def setAddress(self, addrLn1, addrLn2, addrLn3, parish):
        self.address = Address(addrLn1, addrLn2, addrLn3, parish)
    
    def getFullName(self):
        return self.fName + " " + self.lName

    def getAddress(self):
        return self.address.toString()

    def getEmail(self):
        return self.email

#Not to be in final implementation, just testing to see if code works.
if __name__ == "__main__":
    c1 = Customer("Karla", "James", "karlajames@yahoo.com")
    c1.setAddress("Lot 141", "Brunswick Avenue", "Peanut Estates", "St. James")
    print(c1.getFullName())
    print(c1.getAddress())
    print(c1.getEmail())
    


