
class Vehicle:

    def __init__(self, chassisNumber):
        self.chassisNumber = chassisNumber
        
    def setAttr(self, make, model, colour, year, trans, bodyType, mileage, engineNumber, ccRating, price):
        self.make = make
        self.model = model
        self.colour = colour
        self.year = year
        self.trans = trans
        self.bodyType = bodyType
        self.mileage = mileage
        self.engineNumber = engineNumber
        self.ccRating = ccRating
        self.price = price

    def getID(self):
        return self.chassisNumber
        
        
    def getMake(self):
        return self.make
        
        
    def getModel(self):
        return self.model

    def getTitle(self):
        return self.make+" "+self.model
    
    def getColour(self):
        return self.colour
        
        
    def getYear(self):
        return self.year
        
        
    def getTrans(self):
        return self.trans
        
        
    def getbodyType(self):
        return self.bodyType
        
        
    def getMil(self):
        return ("%d MI"%self.mileage)
        
        
    def getEngineNo(self):
        return self.engineNumber
        
        
    def getCCRating(self):
        return ("%d CC"%self.ccRating)
        
    def getPrice(self):
        return ("$ "+str(self.price)+".00")

    def getPriceInt(self):
        return self.price

    def makeObj(self,obj):
        self.chassisNumber = obj['chassisNumber']
        self.make = obj['make']
        self.model = obj['model']
        self.trans = obj['trans']
        self.year = obj['year']
        self.bodyType = obj['bodyType']
        self.engineNumber = obj['engineNumber']
        self.price = obj['price']
        self.ccRating = obj['ccRating']
        self.mileage = obj['mileage']
        self.colour = obj['colour']
