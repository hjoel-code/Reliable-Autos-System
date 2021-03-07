from Persistence.DatabaseManager import DatabaseManager
from Business.Vehicle import Vehicle


class InvoiceManager:

    def __init__(self):
        self.db = DatabaseManager("Invoices")

    def addInvoice(self):
        pass

    def generateInvoicePDF(self):
        pass

    def getAllInvoices(self):
        pass

    def getInvoice(self):
        pass