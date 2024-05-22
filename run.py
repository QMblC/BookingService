from flask import request, render_template, redirect, json
from Location import Location
from Master import Master
from Slot import Slot
import time, threading

from app import db
from app import app

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/addresses/')
def booking():
    array = []
    for i in Location.query.order_by(Location.address).all():
        array.append(i)
    return render_template("addresses.html", locations = array)

@app.route('/addresses/<int:id>/')
def show_location_page(id: int):

    masters = db.session.query(Master).filter(Master.location_id == int(id)).all()

    return render_template('location.html', masters = masters)

@app.route('/create-location/', methods = ['POST', 'GET'])
def create_location():
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

@app.route('/create-master/', methods = ['GET', 'POST'])
def create_master():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        location_id = request.form['location_id']

        try:
            master = Master(first_name = first_name, last_name = last_name, location_id = location_id)

            db.session.add(master)
            db.session.commit()

            master_id = Master.query.all()[-1].id

            slot = Slot(master_id = master_id, booked_by = None)

            db.session.add(slot)

            return redirect('/addresses/')
        except:
            return "Возникла непредвиденная ошибка!"
    else:
        array = []
        for i in Location.query.order_by(Location.address).all():
            array.append(i)
        return render_template("master_form.html", locations = array)
    
@app.route('/addresses/delete/<int:id>')
def delete(id: int):
    location = Location.query.get_or_404(id)

    try:
        db.session.delete(location)
        db.session.commit()
        return redirect('/addresses/')
    except:
        return 'При удалении  произошла ошибка!'
    
@app.route('/masters/delete/<int:id>')
def delete_master(id: int):
    masters = Master.query.get_or_404(id)

    try:
        db.session.delete(masters)
        db.session.commit()
        return redirect('/addresses/')
    except:
        return 'При удалении  произошла ошибка!'
    

@app.route('/api/getaddresses/')
def get():
    array = []
    for i in Location.query.order_by(Location.address).all():
        array.append((i.id, i.address))
    return json.jsonify(array)

app.run(debug=True)

