from datetime import datetime
import random
from Business.Vehicle import Vehicle
from Business.Customer import Customer 

class Discount:
    def __init__(self, title, amount):
        self.title = title
        self.amount = amount

    def getAmount(self):
        return self.amount


class Expense:
    def __init__(self, title, amount):
        self.title = title
        self.amount = amount

    def getAmount(self):
        return self.amount


class Invoice:

    def __init__(self, vehicle=None, customer=None, count=0):
        self.vehicle = vehicle
        self.customer = customer
        self.expense = []
        self.discount = []
        self.date = datetime.now()
        self.GCT = 0.16

        if (count > 0):
            self.id = str(count) + '-' + str(random.randint(1000,9999)) + '-' + str(random.randint(1000,9999))

    def addExpense(self, title, amount):
        expense = Expense(title, amount)
        self.expense.append(expense)

    def addDiscount(self, title, amount):
        discount = Discount(title, amount)
        self.discount.append(discount)

    def getSubTotal(self):
        self.subtotal = int(self.vehicle.price) + self.getTotalExpence() - self.getDiscountAmt()
        return "${:,.2f}".format(float(self.subtotal))


    def getTax(self):
        self.salesTax = self.subtotal * self.GCT
        return "${:,.2f}".format(float(self.salesTax))

    def getTotal(self):
        return "${:,.2f}".format(float(self.subtotal + self.salesTax))
        
    def getDiscountAmt(self):
        summ = 0
        for i in self.discount:
            summ+= i.amount
        return summ
        

    def getTotalExpence(self):
       total = 0
       for x in self.expense:
            total += x.amount
       return total
        

    def getDate(self):
        return self.date

    def toDict(self):
        self.vehicle = self.vehicle.__dict__
        self.customer = self.customer.toDict().__dict__
        
        
        for n in range(len(self.expense)):
            self.expense[n] = self.expense[n].__dict__

        for n in range(len(self.discount)):
            self.discount[n] = self.discount[n].__dict__

        return self

    def toObject(self, doc):
        self.id = doc['id']
        self.date = doc['date']

        self.vehicle = Vehicle()
        self.vehicle.toObject(doc['vehicle'])

        self.customer = Customer()
        self.customer.toObject(doc['customer'])

        for n in range(len(doc['expense'])):
            self.expense.append(Expense(doc['expense'][n]['title'], doc['expense'][n]['amount']))

        for n in range(len(doc['discount'])):
            self.discount.append(Expense(doc['discount'][n]['title'], doc['discount'][n]['amount']))


