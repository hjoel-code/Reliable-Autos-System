class Address:
    def __init__(self, addrLn1, addrLn2, addrLn3, parish):
        self.addrLn1 = addrLn1
        self.addrLn2 = addrLn2
        self.addrLn3 = addrLn3
        self.parish = parish
    
    def toString(self):
        return self.addrLn1 + "\n" + self.addrLn2 + "\n" + self.addrLn3 + "\n" + self.parish
