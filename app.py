from flask import Flask, request, current_app, Response, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
from sqlalchemy.sql import func

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICTATIONS'] = False



db = SQLAlchemy(app)


with app.app_context():
    db.create_all()
