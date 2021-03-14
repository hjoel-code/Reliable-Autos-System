from Persistence.DatabaseManager import DatabaseManager
from Business.Vehicle import Vehicle
from Business.Invoice import Invoice
from firebase_admin import firestore


class InvoiceManager:

    def __init__(self):
        self.db = DatabaseManager("Invoices")

    def addInvoice(self, request):
        count = self.db.getCollectionCount()
        if (count['status']):
            invoice = Invoice(request.vehicle,request.customer,count['data']+1)
            response = self.db.write( invoice.id, invoice.toDict() )
            if response['status'] :
                return {'status':True,'data':invoice.id}
        return count

    def addExpense(self,id,title,expense):
        invoice = Invoice()
        invoice.addExpense(title, expense)
        response = self.db.update(id, {u'expense': firestore.ArrayUnion([u''+ invoice.expense[0].__dict__])})
        
        return True if response['status'] else False

    def addDiscount(self,id,title,discount):
        invoice = Invoice()
        invoice.addDiscount(title, discount)
        response = self.db.update(id, {u'discount': firestore.ArrayUnion([u''+ invoice.discount[0].__dict__])})
        
        return True if response['status'] else False


    def generateInvoicePDF(self):
        pass

    def getAllInvoices(self):
        pass

    def getInvoice(self, id):
        response = self.db.read(id)
        if (not response["status"]):
            response['data'] = None
            return response

        invoice = Invoice()
        invoice.toObject(response['data'].to_dict())

        response['data'] = invoice
        return response  