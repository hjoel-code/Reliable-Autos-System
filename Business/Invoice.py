from datetime import datetime


class Discount:
    def __init__(self, title, amount):
        self.title = title
        self.amount = amount


class Expense:
    def __init__(self, title, amount):
        self.title = title
        self.amount = amount


class Invoice:

    def __init__(self, vehicle, customer):
        self.vehicle = vehicle
        self.customer = customer
        self.expense = []
        self.discount = []
        self.date = datetime.now()
        self.GCT = 0.16

    def addExpense(self, title, amount):
        expense = Expense(title, amount)
        self.expense.append(expense)

    def addDiscount(self, title, amount):
        discount = Discount(title, amount)
        self.discount.append(discount)

    def getGrossAmt(self):
        return float(self.vehicle.price)

    def getFinalAmt(self):
        price = float(self.vehicle.price)
        return (price + self.getTotalExpence()) - self.getDiscountAmt()

   
    def getDiscountAmt(self):
        summ = 0
        for i in self.discount:
            summ+= i.amount
        return summ
        

    def getTotalExpence(self):
       total = 0
       for x in self.expense:
            total += x.amount
       total += total*GCT
       return total
        

    def getDate(self):
        return self.date