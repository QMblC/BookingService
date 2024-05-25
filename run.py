from flask import request, render_template, redirect, json
from Location import Location
from Master import Master
from Slot import Slot
from flask_sqlalchemy import SQLAlchemy
import datetime

from app import db
from app import app

#Автоматическое создание недели


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/addresses/')
def booking():
    array = []
    for i in Location.query.order_by(Location.address).all():
        array.append(i)
    return render_template("addresses.html", locations = array)

@app.route('/addresses/<int:id>/', methods = ['GET', 'POST'])
def view_location_page(id: int):

    if request.method == 'POST':
        date = request.form['date'].split('.')

        day = int(date[0])

        if date[0][0] == '0':
            day = int(date[0][1])

        month = int(date[1])

        if date[1][0] == '0':
            month = int(date[1][1])

        year = int(date[2])

        dt = datetime.datetime(year, month, day, 0, 0, 0)
    else:
        dt = datetime.datetime.now(datetime.timezone.utc)

    masters = []

    masters_people = db.session.query(Master).filter(Master.location_id == int(id)).all()

    for i in range(len(masters_people)):
        person = masters_people[i]

        a = db.session.query(Slot).filter(Slot.master_id == person.id).all()

        person_slots = [x for x in a if x.time.day == dt.day and x.time.month == dt.month]

        masters.append((person, person_slots))


        days = get_next_two_weeks()
        for id, day_info in enumerate(days):
            days[0], days[id] = days[id], days[0]
            if day_info[1] == "{0:02d}.{1:02d}.{2}".format(dt.day, dt.month, dt.year):       
                break

    return render_template('location.html', masters = masters, days = days)

def get_next_two_weeks():
    day = datetime.datetime.now(datetime.timezone.utc)

    days = []

    if day.day + 14 <= day.max.day:
        for i in range(14):
            days.append((get_weekday_string(day.weekday()), "{0:02d}.{1:02d}.{2}".format(day.day, day.month, day.year)))
            if day.day != day.max.day:
                day = datetime.datetime(day.year, day.month, day.day + 1, day.hour, day.minute, day.second)
    else:
        day_counter = 0
        while day.day <= day.max.day:
            day_counter += 1

            days.append((get_weekday_string(day.weekday()), "{0:02d}.{1:02d}.{2}".format(day.day, day.month, day.year)))
            if day.day != day.max.day:
                day = datetime.datetime(day.year, day.month, day.day + 1, day.hour, day.minute, day.second)
            else:
                break

        day = datetime.datetime(day.year, day.month + 1, 1, day.hour, day.minute, day.second)
        for i in range(14 - day_counter):
            days.append((get_weekday_string(day.weekday()), "{0:02d}.{1:02d}.{2}".format(day.day, day.month, day.year)))
            day = datetime.datetime(day.year, day.month, day.day + 1, day.hour, day.minute, day.second)
    
    return days

def get_weekday_string(weekday: int):
    if weekday == 0:
        return "Понедельник"
    elif weekday == 1:
        return "Вторник"
    elif weekday == 2:
        return "Среда"
    elif weekday == 3:
        return "Четверг"
    elif weekday == 4:
        return "Пятница"
    elif weekday == 5:
        return "Суббота"
    elif weekday == 6:
        return "Воскресенье"
    else:
        raise ValueError("weekday value is incorrect")

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

            add_slot_db(db, master_id)
            
            return redirect('/addresses/')
        except:
            return "Возникла непредвиденная ошибка!"
    else:
        array = []
        for i in Location.query.order_by(Location.address).all():
            array.append(i)
        return render_template("master_form.html", locations = array)
    
def add_slot_db(db: SQLAlchemy, master_id):
    dt = datetime.datetime.now(datetime.timezone.utc)
    start_dt = datetime.datetime(dt.year, dt.month, dt.day, 9, 0, 0)

    new_dt = start_dt
    for i in range(4):
        for j in range(7):
            for k in range(22):
                if k % 2 == 0:
                    hrs = 0
                else:
                    hrs = 1
                slot = Slot(master_id = master_id, booked_by = None, slot_type = "empty", time = new_dt)
                db.session.add(slot)
                new_dt = datetime.datetime(new_dt.year, new_dt.month, new_dt.day, new_dt.hour + hrs, (new_dt.minute + 30) % 60, new_dt.second)
            if new_dt.day == new_dt.max.day:
                if new_dt.month == 12:
                    new_dt = datetime.datetime(new_dt.year + 1, 1, 1, 9, 0, 0)
                else:
                    new_dt = datetime.datetime(new_dt.year, new_dt.month + 1, 1, 9, 0, 0)
            else:
                new_dt = datetime.datetime(new_dt.year, new_dt.month, new_dt.day + 1, 9, 0, 0)
            
    db.session.commit()


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
        return 'При удалении произошла ошибка!'
    

@app.route('/api/getaddresses/')
def get():
    array = []
    for i in Location.query.order_by(Location.address).all():
        array.append((i.id, i.address))
    return json.jsonify(array)

if __name__ == "__main__":
    app.run(port = 5000, debug=True)


