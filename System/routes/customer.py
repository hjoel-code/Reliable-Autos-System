from flask import Flask, render_template, request, redirect, url_for, flash, make_response, Blueprint
from ..model import customerUI



customer = Blueprint('customer', __name__, template_folder='templates', static_folder='static')

@customer.route('/search', methods=["GET","POST"])
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

@customer.route('/inventory/vehicle/<vid>')
def viewVehicle(vid):
    vehicle = customerUI.viewVehicle(vid)
    
    if (vehicle["status"]):
        
        inventory = customerUI.filterInventory("", "", vehicle["data"].bodyType, vehicle["data"].trans, vehicle["data"].year, "99999")
        return render_template("vehicle-template.html", title = "Used " + vehicle["data"].getTitle(), vehicle = vehicle["data"], inventory = inventory['data'])
    flash("Error: Something went wrong")
    return redirect(url_for("home"))

@customer.route('/inventory/vehicle/<vid>/request', methods=['GET', 'POST'])
def addRequestAction(vid):
    if (request.method == 'POST'):
        response = customerUI.sendRequest(vid, request.form['firstName'], request.form['lastName'], request.form['email'], request.form['requestType'], request.form['custom-message'])
        flash("Request Successfully Sent")
        return redirect("/inventory/vehicle/"+vid)
    flash("Error: Something went wrong")
    return redirect("/inventory/vehicle/"+vid)
