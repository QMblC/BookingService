from flask import Flask
from flask import request
from flask import jsonify
import flask

name = 'name'

app = Flask(name)

@app.route('/hello')
def hello():
    return "hello"

@app.route('/echo')
def headers():
   value = request.headers
   dic = dict()
   for i in value:
      dic[i[0]] = i[1]
   return jsonify(dic)

   #return jsonify(request.headers.values)

@app.route('/echo', methods = ['POST'])
def a():
   body = request.form['name']
   return body

@app.route('/main')
def main():
  return flask.render_template('index.html')

if name == 'name':
  app.run(debug=True)