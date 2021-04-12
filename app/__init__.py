# EXTERNAl IMPORTS
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, Blueprint
from flask_dropzone import Dropzone

# INTERNAL IMPORTS
from config import app
from .packages import adminUI, customerUI, auth

# BLUEPRINTS
from .views.admin import admin
from .views.customer import customer


dropzone = Dropzone(app)
app.register_blueprint(admin)
app.register_blueprint(customer)


@app.route('/')
def home():
    inventory = customerUI.viewInventory()
    if (inventory["status"]):
        return render_template("index.html", count = len(inventory['data']), inventory = inventory["data"])
    return render_template("index.html")

