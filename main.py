from flask import Flask, render_template, request, redirect, url_for

from Presentation.AdminUI import AdminUI
from Presentation.CustomerUI import CustomerUI
from Business.InventoryManager import InventoryManager
from os import system, name 

app = Flask(__name__)
adminUI = AdminUI()
customerUI = CustomerUI()
db = InventoryManager()

@app.route('/admin')
@app.route('/admin')
def login():
    return render_template("admin/auth/login.html")

@app.route('/admin', methods=['GET', 'POST'])
def loginAction():
    if (request.method == 'POST'):
        return redirect(url_for('adminMenu'))
    else:
        error = 'Invalid username/password'
        return render_template('login.html', error=error)


@app.route('/admin/auth/signUp')
def signUp():
    return render_template("admin/auth/signUp.html")


@app.route('/admin/menu')
def adminMenu():
    return render_template("admin/menu.html", name = 'Joel Henry')


@app.route('/admin/add-to-inventory')
def addVehicle():
    return render_template('admin/add-to-inventory.html')


@app.route('/admin/add-to-inventory', methods=['GET', 'POST'])
def addVehicleAction():
    if (request.method == 'POST'):
        response = adminUI.addVehicle(request.form['chassis'], request.form['make'], request.form['model'],request.form['year'], request.form['price'], 'Black' ,request.form['trans'], request.form['type'], request.form['mil'],request.form['engine'], request.form['cc'])
        
        if (response["status"]):
            return redirect(url_for('adminMenu'), success = "add-to-inventory")

        return render_template(url_for('addVehicle'), error = ["add-to-inventory"], message = "")
    return  render_template(url_for('addVehicle'), error = ["add-to-inventory"], message = "")

@app.route('/admin/inventory')
def inventory():
    inventory = db.getInventory()

    if (inventory["status"]):
        return render_template("admin/inventory.html", count = len(inventory['data']), inventory = inventory["data"])
    return render_template("admin/inventory.html", error = ["inventory-error"], message = "")


@app.route('/admin/inventory/update-remove')
def removeInventory():
    inventory = db.getInventory()

    if (inventory["status"]):
        return render_template("admin/inventory-update.html", inventory = inventory["data"], task = "remove")
    return render_template("admin/inventory-update.html", error = ["inventory-remove-error"], message = "", task = "remove")

@app.route('/admin/inventory/update')
def updateInventory():
    inventory = db.getInventory()

    if (inventory["status"]):
        return render_template("admin/inventory-update.html", inventory = inventory["data"], task = "remove")
    return render_template("admin/inventory-update.html", error = ["inventory-edit-error"], message = "", task = "edit")


@app.route('/admin/inventory/update-remove/<vid>')
def removeVehicle(vid):
    response = adminUI.removeVehicle(vid)

    if (response["status"]):
        inventory = db.getInventory()

        if (inventory["status"]):
            return render_template("admin/inventory.html", count = len(inventory['data']), inventory = inventory["data"], task = "remove", success = "remove-success")
        return render_template("admin/inventory-update.html", error = ["inventory-edit-error"], inventory = inventory["data"], task = "remove", success = "remove-success")
    return render_template("admin/inventory-update.html", error = ["inventory-edit-error", "remove-error"], count = len(inventory['data']), inventory = inventory["data"], task = "remove", success = "remove-success")
    
@app.route('/')
def home():
    inventory = db.getInventory()

    if (inventory["status"]):
        return render_template("index.html", count = len(inventory['data']), inventory = inventory["data"])
    return render_template("index.html", error = ["inventory-error"], message = "")

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
        return render_template("index.html", error = ["inventory-error"], message = "")
    
    inventory = db.getInventory()

    if (inventory["status"]):
        return render_template("index.html", error = ["filter-error"], count = len(inventory['data']), inventory = inventory["data"])
    return render_template("index.html", error = ["inventory-error","filter-error"], message = "")


if __name__ == "__main__":
    
    app.run(debug=True)



        
