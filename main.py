from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from urllib.parse import urlparse
import pdfkit

from Presentation.UI import AdminUI
from Presentation.UI import CustomerUI
from Security.Authentication import Authentication

from os import system, name 

from flask_dropzone import Dropzone


app = Flask(__name__)
dropzone = Dropzone(app)

adminUI = AdminUI()
customerUI = CustomerUI()
auth = Authentication()


@app.route('/admin/sign-out')
def signout():
    auth.signOut()
    return redirect(url_for('home'))

@app.route('/admin')
def login():
    if (not auth.isUser):
        return render_template("admin/auth/login.html")
    return redirect(url_for('adminMenu'))

@app.route('/admin', methods=['GET', 'POST'])
def loginAction():
    if (request.method == 'POST'):
        response = auth.signIn(request.form['email'], request.form['password'])
        if (response['status']):
            return redirect(url_for('adminMenu'))
        else:
            return render_template("admin/auth/login.html", error = response['error'])
    return redirect(url_for('login'))

@app.route('/admin/auth/signUp')
def signUp():
    if (auth.isUser):
        return render_template("admin/auth/signUp.html")
    return redirect(url_for('login'))

@app.route('/admin/auth/sign/new', methods =['GET', 'POST'])
def signUpAction():
    if (auth.isUser):
        if (request.method == 'POST'):
            if (request.form['password'] == request.form['confirm-password']):
                response = adminUI.addNewAdministrator(request.form['first-name'], request.form['last-name'], request.form['email'], request.form['password'])
            else:
                return render_template("admin/auth/signUp.html", error = "Password Doesn't Match", form = request.form)
            
            if (response['status']):
                return redirect(url_for('adminMenu', __METHOD_OVERRIDE__ = 'POST', success=True, message = 'New Administrator Successfully Added'))
            return render_template("admin/auth/signUp.html", error = response['error'], form = request.form)

    return redirect(url_for('login'))

@app.route('/admin/menu', methods = ['GET', 'POST'])
def adminMenu():
    if (auth.isUser):
        if (request.method == 'POST'):
            print(request.form['success'], request.form['message'])
        return render_template("admin/menu.html", name = auth.user.getDisplayName(), success = None, message = '')
    return redirect(url_for('login'))





@app.route('/admin/add-to-inventory')
def addVehicle():
    if (auth.isUser):
        return render_template('admin/add-to-inventory.html')
    return redirect(url_for('login'))

@app.route('/admin/add-to-inventory/upload', methods=['GET', 'POST'])
def addVehicleAction():
    if (auth.isUser):
        if (request.method == 'POST'):
            
            response = adminUI.addVehicle(request.form['chassis'], request.form['make'], request.form['model'], request.form['colour'], request.form['year'], request.form['trans'], request.form['type'], request.form['mil'],request.form['engine'], request.form['price'], request.form['priceStatus'], request.form['location'], request.form['description']) 
            
            if (response["status"]):
                return render_template("admin/img-upload-template.html", vid = request.form['chassis'], success = "add-to-inventory", make = request.form['make'], model = request.form['model'], year = request.form['year'])

            return render_template(url_for('addVehicle'), error = True, message = "")
        return  render_template(url_for('addVehicle'), error = True, message = "")
    return redirect(url_for('login'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ['jpg', 'png', 'jpeg']

@app.route('/upload/<vid>', methods=['GET', 'POST'])
def addImagesAction(vid):
    if request.method == 'POST':

        if 'file' not in request.files:
            print('No file part')
            return "No file", 400

        img = request.files['file']

        if img.filename == '':
            print('No selected file')
            return "No selected file", 400

        if img and allowed_file(img.filename):
            print('File successfully uploaded') if adminUI.addImages(vid, img) else print("Failed to upload Image") 
            return "Successfully Uploaded", 200
        else:
            print('Wrong File Type')
            return "Wrong File Type", 400

@app.route('/admin/inventory')
def inventory():
    if (auth.isUser):
        inventory = adminUI.viewInventory()

        if (inventory["status"]):
            return render_template("admin/inventory.html", count = len(inventory['data']), inventory = inventory["data"])
        return render_template("admin/inventory.html", error = True, message = "")
    return redirect(url_for('login'))




@app.route('/admin/inventory/update-remove')
def removeInventory():
    if (auth.isUser):
        inventory = adminUI.viewInventory()

        if (inventory["status"]):
            return render_template("admin/inventory-update.html", inventory = inventory["data"], task = "remove")
        return render_template("admin/inventory-update.html", error = True, message = "", task = "remove")
    return redirect(url_for('login'))

@app.route('/admin/inventory/update')
def updateInventory():
    if (auth.isUser):
        inventory = adminUI.viewInventory()

        if (inventory["status"]):
            return render_template("admin/inventory-update.html", inventory = inventory["data"], task = "edit")
        return render_template("admin/inventory-update.html", error = True, message = "", task = "edit")
    return redirect(url_for('login'))

@app.route('/admin/inventory/update-remove/<vid>')
def removeVehicle(vid):
    if auth.isUser :
        response = adminUI.removeVehicle(vid)

        if (response["status"]):
            return redirect(url_for('removeInventory'))
        return render_template("admin/inventory-update.html", error = True, count = len(inventory['data']), inventory = inventory["data"], task = "remove", success = "remove-success")
    return redirect(url_for('login'))

@app.route('/admin/inventory/update/<vid>')
def editVehicle(vid):
    if auth.isUser :
        response = adminUI.viewVehicle(vid)

        if (response["status"]):
            return render_template('admin/vehicle-template.html', vehicle = response['data'])
        
        return redirect(url_for('updateInventory'))
    return redirect(url_for('login'))





@app.route('/admin/requests')
def viewRequest():
    if (auth.isUser):
        response = adminUI.viewAllReaquests()

        if (response["status"]):
            return render_template("admin/all-requests.html", requests = response['data'], count = len(response['data']))
        return render_template(url_for('adminMenu'))
    return redirect(url_for('login'))

@app.route('/admin/request/<id>')
def requestDetails(id):
    if (auth.isUser):
        response = adminUI.viewRequest(id)

        if (response['status']):
            return render_template("admin/request-template.html", request = response['data'])
        return render_template(url_for('viewRequest'))
    return redirect(url_for('login'))

@app.route('/admin/invoice')
def viewInvoices():
    if auth.isUser :
        response = adminUI.viewAllInvoices()

        if (response["status"]):
            return render_template("admin/all-invoices.html", invoices = response['data'], count = len(response['data']))
        return render_template(url_for('adminMenu'))
    return redirect(url_for('login'))

@app.route('/admin/invoice-details/<id>')
def invoiceDetails(id):
    if auth.isUser :
        response = adminUI.viewInvoice(id)

        if (response['status']):
            return render_template("admin/invoice.html", invoice = response['data'])
        return render_template(url_for('viewInvoices'))
    return redirect(url_for('login'))

@app.route('/add-exp/<id>', methods = ['GET', 'POST'])
def addExpenseAction(id):
    if (request.method == 'POST'):
        response = adminUI.addInvoiceExpense(id, request.form['title'], request.form['amount'])
        return redirect(request.host_url+'admin/invoice-details/'+id, 301)
    return '',400

@app.route('/add-disc/<id>', methods = ['GET', 'POST'])
def addDiscountAction(id):
    if (request.method == 'POST'):
        response = adminUI.addInvoiceDiscount(id, request.form['title'], request.form['amount'])
        return redirect(request.host_url+'admin/invoice-details/'+id, 301)
    return '',400

@app.route('/admin/invoice-request/<id>')
def generateInvoiceFromRequest(id):
    if (auth.isUser):
        response = adminUI.viewRequest(id)
        if (response['status']):
            if (response['data'].invoice == ''):
                response = adminUI.addInvoice(response['data'])
                if (response['status']):
                    adminUI.request.updateRequestField(id,'invoice',response['data'])
                    response = adminUI.generateInvoice(response['data'])
                    return redirect('/admin/invoice-details/' + response['data'].id, 301)

        return '', 404
    return redirect(url_for('login'))

@app.route('/admin/invoice/<id>')
def generateInvoice(id):
    if auth.isUser:
        response = adminUI.generateInvoice(id)

        if (response['status']):

            rendered = render_template('invoice-template.html', invoice = response['data'], title = 'Invoice No. ' + response['data'].id)
            pdf = pdfkit.from_string(rendered, False)

            responseHttp = make_response(pdf)
            responseHttp.headers['Content-Type'] = 'application/pdf'
            responseHttp.headers['Content-Disposition'] = 'inline; filename=Invoice No. ' + response['data'].id + '.pdf'

            return responseHttp

        return '', 404
    return redirect(url_for('login'))



@app.route('/')
def home():
    inventory = customerUI.viewInventory()

    if (inventory["status"]):
        return render_template("index.html", count = len(inventory['data']), inventory = inventory["data"])
    return render_template("index.html", error = True, message = "")

@app.route('/search', methods=["GET","POST"])
def filterInventory():
    if (request.method == 'GET'):
        make = "" if request.args['make'] == 'any' else request.args['make']
        model = "" if request.args['model'] == 'any' else request.args['model']
        bType = "" if request.args['bType'] == 'any' else request.args['bType']
        trans = "" if request.args['trans'] == 'any' else request.args['trans']
        yearMin = request.args['yearMin']
        yearMax = request.args['yearMax']
        inventory = customerUI.filterInventory(make, model, bType, trans, yearMin, yearMax)
        if (inventory["status"]):
            return render_template("index.html", count = len(inventory['data']), inventory = inventory["data"])
        return render_template("index.html", error = True, message = "")
    
    inventory = customerUI.viewInventory()

    if (inventory["status"]):
        return render_template("index.html", error = True, count = len(inventory['data']), inventory = inventory["data"])
    return render_template("index.html", error = True, message = "")

@app.route('/inventory/vehicle/<vid>')
def viewVehicle(vid):
    vehicle = customerUI.viewVehicle(vid)
    
    if (vehicle["status"]):
        
        inventory = customerUI.filterInventory("", "", vehicle["data"].bodyType, vehicle["data"].trans, vehicle["data"].year, "99999")
        return render_template("vehicle-template.html", title = "Used " + vehicle["data"].getTitle(), vehicle = vehicle["data"], inventory = inventory['data'])
    return render_template("index.html", error = True, message = "")

@app.route('/inventory/vehicle/<vid>/request', methods=['GET', 'POST'])
def addRequestAction(vid):
    if (request.method == 'POST'):
        response = customerUI.sendRequest(vid, request.form['firstName'], request.form['lastName'], request.form['email'], request.form['requestType'], request.form['custom-message'])
        return redirect("/inventory/vehicle/"+vid)
    return redirect("/inventory/vehicle/"+vid)



@app.route('/<id>/<token>')
def customerInfo(id, token):
    response = adminUI.viewRequest(id)
    if ((response['data'].token == token) and response['status']):
        return render_template("customer-info.html", request=response['data'], vehicle=response['data'].vehicle, customer=response['data'].customer, tokenValid=response['data'].tokenValid)
    return render_template("customer-info.html", tokenValid=False)

@app.route('/submit/<id>/<token>',methods=['GET', 'POST'])
def submitCustomerInfo(id, token):
    if (request.method == 'POST'):
        response = adminUI.viewRequest(id)
        print(response)
        if ((response['data'].token == token) and response['status']):
            
            response = adminUI.addCustomerAddress(request.form['first-name'], request.form['last-name'], request.form['addr1'], request.form['addr2'], request.form['addr3'], request.form['parish'], response['data'])
            
            if (response['status']):
                print("Success")
                return render_template("customer-info.html", submit = True)
    
    return render_template("customer-info.html", submit = False)


if __name__ == "__main__": 
    app.secret_key = "AIzaSyBrZVMANrVDDLuqYJktyTDolrDsSDNyZHc"
    app.run(debug=True)



        
