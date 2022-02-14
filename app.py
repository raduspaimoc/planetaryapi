from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY'] = 'super-secret' #change this IRL
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)


from Planet import Planet, planet_schema, planets_schema
from User import User, user_schema, users_schema



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
                     home_start="Home Star",
                     mass=3.258e23,
                     radius=1516,
                     distance=35.98e6)

    venus = Planet(planet_name="Venus",
                     planet_type="Class K",
                     home_start="Sol",
                     mass=4.458e23,
                     radius=10046,
                     distance=20.98e6)

    earth = Planet(planet_name="Mercury",
                     planet_type="Class A",
                     home_start="Sol",
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


@app.route('/planets', methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(result)


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created successfully'), 201


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='Login succeeded', access_token=access_token)
    else:
        return jsonify(message='Bad email or password'), 401


@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email: str):
    user = User.query.filter_by(email=email).first()
    if user:
        msg = Message("Your planetary API password is " + user.password,
                      sender="admin@planetary-api.com",
                      recipients=[email])
        mail.send(msg)
        return jsonify(message='Password sent to ' + email)
    else:
        return jsonify(message="That email doesn't exist"), 401



if __name__ == '__main__':
    app.run()
