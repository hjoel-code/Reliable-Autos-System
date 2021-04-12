from flask import Flask, render_template, request, redirect, url_for, flash, make_response, Blueprint
from ..system import pdfkit, adminUI, auth


admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


# User Authentication related routes
@admin.route('/admin')
def login():
    if (not auth.isUser):
        return render_template("admin/auth/login.html")
    return redirect(url_for('admin.adminMenu'))

@admin.route('/admin', methods=['GET', 'POST'])
def loginAction():
    if (request.method == 'POST'):
        response = auth.signIn(request.form['email'], request.form['password'])
        if (response['status']):
            flash("WELCOME BACK " + auth.user.getDisplayName())
            return redirect(url_for('admin.adminMenu'))
        else:
            flash("Error: Something went wrong")
            return redirect(url_for('admin.login'))
    flash("Error: Something went wrong")
    return redirect(url_for('admin.login'))

@admin.route('/admin/auth/signUp')
def signUp():
    if (auth.isUser):
        return render_template("admin/auth/signUp.html")
    flash("Error: Registered Users Only")
    return redirect(url_for('admin.login'))

@admin.route('/admin/auth/sign/new', methods =['GET', 'POST'])
def signUpAction():
    if (auth.isUser):
        if (request.method == 'POST'):
            if (request.form['password'] == request.form['confirm-password']):
                response = adminUI.addNewAdministrator(request.form['first-name'], request.form['last-name'], request.form['email'], request.form['password'])
            else:
                flash("Error: Password doesn't match")
                return render_template("admin/auth/signUp.html", form = request.form)
            
            if (response['status']):
                flash("New administrator successfully added")
                return redirect(url_for('admin.adminMenu'))
            flash("Error: Something went wrong")
            return render_template("admin/auth/signUp.html", form = request.form)
    flash("Error: Registered Users Only")
    return redirect(url_for('admin.login'))

@admin.route('/admin/sign-out')
def signout():
    auth.signOut()
    return redirect(url_for('home'))


# Administration Home route
@admin.route('/admin/menu', methods = ['GET', 'POST'])
def adminMenu():
    if (auth.isUser):
        return render_template("admin/menu.html", name = auth.user.getDisplayName(), success = None, message = '')
    flash("Error: Registered Users Only")
    return redirect(url_for('admin.login'))



# Inventory Manipulation related routes
@admin.route('/admin/add-to-inventory')
def addVehicle():
    if (auth.isUser):
        return render_template('admin/add-to-inventory.html')
    flash("Error: Registered Users Only")
    return redirect(url_for('admin.login'))

@admin.route('/admin/add-to-inventory/upload', methods=['GET', 'POST'])
def addVehicleAction():
    if (auth.isUser):
        if (request.method == 'POST'):
            
            response = adminUI.addVehicle(request.form['chassis'], request.form['make'], request.form['model'], request.form['colour'], request.form['year'], request.form['trans'], request.form['type'], request.form['mil'],request.form['engine'], request.form['price'], request.form['priceStatus'], request.form['location'], request.form['description']) 
            
            if (response["status"]):
                flash("Successfully added "+request.form['make']+" "+request.form['model']+" "+request.form['year'])
                return render_template("admin/img-upload-template.html", vid = request.form['chassis'])
            flash("Error: Failed to Add Vehicle to Inventory")
            return render_template(url_for('admin.addVehicle'))
        flash("Error: Failed to Add Vehicle to Inventory")
        return  render_template(url_for('admin.addVehicle'))
    flash("Error: Registered Users Only")
    return redirect(url_for('admin.login'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ['jpg', 'png', 'jpeg']

@admin.route('/upload/<vid>', methods=['GET', 'POST'])
def addImagesAction(vid):
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('Error: No file part')
            return "No file", 400

        img = request.files['file']

        if img.filename == '':
            flash('Error: No selected file')
            return "No selected file", 400

        if img and allowed_file(img.filename):
            flash('File successfully uploaded') if adminUI.addImages(vid, img) else flash("Error: Failed to upload Image") 
            return "Successfully Uploaded", 200
        else:
            flash('Error: Wrong File Type')
            return "Wrong File Type", 400

@admin.route('/admin/inventory/update')
def updateInventory():
    if (auth.isUser):
        inventory = adminUI.viewInventory()

        if (inventory["status"]):
            return render_template("admin/inventory-update.html", inventory = inventory["data"], task = "edit")
        flash("Error: Failed to load Inventory")
        return render_template("admin/inventory-update.html")
    flash("Error: Registered Users Only")
    return redirect(url_for('admin.login'))

@admin.route('/admin/inventory/update-remove/<vid>')
def removeVehicle(vid):
    if auth.isUser :
        response = adminUI.removeVehicle(vid)

        if (response["status"]):
            flash("Successfully Removed")
            return redirect(url_for('admin.updateInventory'))
        flash("Error: Failed to remove vehicle from Inventory")
        return redirect(url_for('admin.updateInventory'))
    flash("Error: Registered Users Only")
    return redirect(url_for('admin.login'))

@admin.route('/admin/inventory/update/<vid>')
def editVehicle(vid):
    if auth.isUser :
        response = adminUI.viewVehicle(vid)

        if (response["status"]):
            return render_template('admin/vehicle-template.html', vehicle = response['data'])
        flash("Error: Failed to load Vehicle Information")
        return redirect(url_for('admin.updateInventory'))
    flash("Error: Registered Users Only")
    return redirect(url_for('admin.login'))

@admin.route('/submit-changes/vehicle/<vid>', methods=['GET', 'POST'])
def submitVehicleEdits(vid):
    if (request.method == 'POST'):
        adminUI.submitVehicleUpdates(vid, request.form)
        flash("Updates Successfully Registered")
        return redirect(url_for("admin.updateInventory"))
    flash("Error: Failed to register updates")
    return redirect("/admin/inventory/update/"+vid)


# Request Management related routes
@admin.route('/admin/requests')
def viewRequest():
    if (auth.isUser):
        response = adminUI.viewAllReaquests()

        if (response["status"]):
            return render_template("admin/all-requests.html", requests = response['data'], count = len(response['data']))
        flash("Error: Failed to load request")
        return render_template(url_for('adminMenu'))
    flash("Error: Registered Users Only")
    return redirect(url_for('admin.login'))

@admin.route('/admin/request/<id>')
def requestDetails(id):
    if (auth.isUser):
        response = adminUI.viewRequest(id)

        if (response['status']):
            return render_template("admin/request-template.html", request = response['data'])
        flash("Error: Failed to load Request ("+id+")")
        return render_template(url_for('admin.viewRequest'))
    flash("Error: Registered Users Only")
    return redirect(url_for('admin.login'))


# Invoice Management related routes
@admin.route('/admin/invoice')
def viewInvoices():
    if auth.isUser :
        response = adminUI.viewAllInvoices()

        if (response["status"]):
            return render_template("admin/all-invoices.html", invoices = response['data'], count = len(response['data']))
        flash("Error: Failed to load Invoices")
        return render_template(url_for('admin.adminMenu'))
    flash("Error: Registered Users Only")
    return redirect(url_for('admin.login'))

@admin.route('/admin/invoice-details/<id>')
def invoiceDetails(id):
    if auth.isUser :
        response = adminUI.generateInvoice(id)

        if (response['status']):
            return render_template("admin/invoice.html", invoice = response['data'])
        
        flash("Error: Failed to load Invoice")
        return render_template(url_for('admin.viewInvoices'))
    flash("Error: Registered Users Only")
    return redirect(url_for('admin.login'))

@admin.route('/add-exp/<id>', methods = ['GET', 'POST'])
def addExpenseAction(id):
    if (request.method == 'POST'):
        response = adminUI.addInvoiceExpense(id, request.form['title'], request.form['amount'])
        flash("Expense Successfully added")
        return redirect(request.host_url+'admin/invoice-details/'+id, 301)
    flash("Error: Failed to add Expense")
    return redirect(request.host_url+'admin/invoice-details/'+id, 301)

@admin.route('/add-disc/<id>', methods = ['GET', 'POST'])
def addDiscountAction(id):
    if (request.method == 'POST'):
        response = adminUI.addInvoiceDiscount(id, request.form['title'], request.form['amount'])
        flash("Discount Successfully added")
        return redirect(request.host_url+'admin/invoice-details/'+id, 301)
    flash("Error: Failed to add Discount")
    return redirect(request.host_url+'admin/invoice-details/'+id, 301)

@admin.route('/admin/invoice-from-request/<request_id>')
def generateInvoiceFromRequest(request_id):
    if (auth.isUser):
        response = adminUI.generateInvoiceFromRequest(request_id)
        if (response['status']):
            flash("Successfully Generated Invoice")
            return redirect('/admin/invoice-details/' + response['data'].id, 301)
        flash("Error: Failed to Generated Invoice")
        return '', 404
    flash("Error: Registered Users Only")
    return redirect(url_for('admin.login'))

@admin.route('/admin/invoice/<id>')
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
    flash("Error: Registered Users Only")
    return redirect(url_for('admin.login'))

@admin.route('/<id>/<token>')
def customerInfo(id, token):
    response = adminUI.viewRequest(id)
    if ((response['data'].token == token) and response['status']):
        return render_template("customer-info.html", request=response['data'], vehicle=response['data'].vehicle, customer=response['data'].customer, tokenValid=response['data'].tokenValid)
    return render_template("customer-info.html", tokenValid=False)

@admin.route('/submit/<id>/<token>',methods=['GET', 'POST'])
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

