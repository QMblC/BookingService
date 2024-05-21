from flask import Flask, request, current_app, Response, render_template, redirect, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from Location import Location

from app import db
from app import app

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/addresses/')
def booking():
    array = []
    for i in Location.query.order_by(Location.address).all():
        array.append(i.address)
    return render_template("addresses.html", locations= array)

@app.route('/create/', methods = ['POST', 'GET'])
def create():
    if request.method == 'POST':
        address = request.form['address']
        location = Location(address = address)

        try:
            db.session.add(location)
            db.session.commit()
            return redirect('/addresses/')
        except:
            pass
    else:
        return render_template("location_form.html")

@app.route('/api/getaddresses/')
def get():
    array = []
    for i in Location.query.order_by(Location.address).all():
        array.append((i.id, i.address))
    return json.jsonify(array)

app.run(debug=True)