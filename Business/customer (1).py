import Address

class Customer:
    #Constructor to initialise customer
    def __init__(self, fName, lName, email):
        self.fName = fName
        self.lName = lName
        self.email = email

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

# #Not to be in final implementation, just testing to see if code works.
# if __name__ == "__main__":
#     c1 = Customer("Karla", "James", "karlajames@yahoo.com")
#     c1.setAddress("Lot 141", "Brunswick Avenue", "Peanut Estates", "St. James")
#     print(c1.getFullName())
#     print(c1.getAddress())
#     print(c1.getEmail())
    


