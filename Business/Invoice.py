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

    def getNetAmt(self):
        price = float(self.vehicle.price)
        return (price + self.getTotalExpence()) - self.getDiscountAmt()

    def getDiscountAmt(self):
        pass

    def getTotalExpence(self):
        pass

    def getDate()
        pass