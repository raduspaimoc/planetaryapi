from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///' + os.path.join(basedir, 'planets.db')
db = SQLAlchemy(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/super_simple')
def super_simple():  # put application's code here
    return jsonify(message='Hello worlllld ')


@app.route('/not_found')
def not_found():  # put application's code here
    return jsonify(message='The resource was not found'), 400


@app.route('/parameters')
def params():  # put application's code here
    name = request.args.get("name")
    age = int(request.args.get("age"))
    if age < 18:
        return jsonify(message='Sorry ' + name + "you are not old enough."), 401
    else:
        return jsonify(message='Congrats ' + name + "you are not old enough.")


@app.route('/params/<string:name>/<int:age>')
def parameters(name: str, age: int):  # put application's code here
    if age < 18:
        return jsonify(message='Sorry ' + name + "you are not old enough."), 401
    else:
        return jsonify(message='Congrats ' + name + "you are not old enough.")
    

if __name__ == '__main__':
    app.run()
