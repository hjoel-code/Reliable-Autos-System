
class Vehicle:
    def __init__(self):
        self.images = ["https://firebasestorage.googleapis.com/v0/b/javvy-s-autozone.appspot.com/o/assets%2Fno-image.jpg?alt=media&token=5eba1699-aff8-4206-bca5-2a591597d179"]
        self.displayImage = "https://firebasestorage.googleapis.com/v0/b/javvy-s-autozone.appspot.com/o/assets%2Fno-image.jpg?alt=media&token=5eba1699-aff8-4206-bca5-2a591597d179"
        self.description = ""
        self.vehicleStatus = "Available"
        
    def newVehicle(self, chassis, make, model, colour, year, trans, bodyType, mileage, engineNumber, price, priceStatus, location, description):
        self.make = make
        self.model = model
        self.colour = colour
        self.year = year
        self.trans = trans
        self.bodyType = bodyType
        self.mileage = mileage
        self.engineNumber = engineNumber
        self.price = price
        self.priceStatus = priceStatus
        self.location = location
        self.description = description
        self.id = chassis 

    def setImages(self, images, displayImage):
        self.images = images
        self.displayImage = displayImage

    def addImage(self, image):
        if (self.images[0] == "https://firebasestorage.googleapis.com/v0/b/javvy-s-autozone.appspot.com/o/assets%2Fno-image.jpg?alt=media&token=5eba1699-aff8-4206-bca5-2a591597d179"):
            self.images = []
        self.images.append(image)

    def getTitle(self):
        return self.year+" "+self.make+" "+self.model
        
    def getPrice(self):
        return "${:,.2f}".format(float(self.price))

    
    def toObject(self,obj):
        self.make = obj['make']
        self.model = obj['model']
        self.trans = obj['trans']
        self.year = obj['year']
        self.bodyType = obj['bodyType']
        self.engineNumber = obj['engineNumber']
        self.price = obj['price']
        self.mileage = obj['mileage']
        self.colour = obj['colour']
        self.priceStatus = obj['priceStatus']
        self.location = obj['location']
        self.description = obj['description']
        self.id = obj['id']
        self.images = obj['images']
        self.displayImage = obj['displayImage']
        self.vehicleStatus = obj['vehicleStatus']