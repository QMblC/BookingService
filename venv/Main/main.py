from flask import Flask, request, current_app, Response, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("main/index.html")

@app.route('/booking/')
def booking():
    return render_template("main/booking.html")



app.run(debug=True)
    