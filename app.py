from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os

from Planet import Planet
from User import User

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///' + os.path.join(basedir, 'planets.db')
db = SQLAlchemy(app)


@app.cli.command("db_create")
def db_create():
    db.create_all()
    print("Database created!")


@app.cli.command("db_drop")
def db_drop():
    db.drop_all()
    print("Database dropped!")


@app.cli.command("db_seed")
def db_seed():
    mercury = Planet(planet_name="Mercury",
                     planet_type="Class D",
                     home_star="Home Star",
                     mass=3.258e23,
                     radius=1516,
                     distance=35.98e6)

    venus = Planet(planet_name="Venus",
                     planet_type="Class K",
                     home_star="Sol",
                     mass=4.458e23,
                     radius=10046,
                     distance=20.98e6)

    earth = Planet(planet_name="Mercury",
                     planet_type="Class A",
                     home_star="Sol",
                     mass=1.258e23,
                     radius=100,
                     distance=10.98e6)

    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(first_name="William",
                     last_name="Herschel",
                     email="william@mail.com",
                     password="1234")

    db.session.add(test_user)
    db.session.commit()

    print("Database seeded!")


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
