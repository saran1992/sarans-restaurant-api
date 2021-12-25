from flask import Flask, jsonify,request
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db/restaurant.db')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("DB created successfully!")

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("DB dropped!")

@app.cli.command('db_seed')
def db_seed():
    pizza = Dish(name = "pizza",
                 price = 59.99,
                 rating = 5,
                 number_of_reviews = 1)
    db.session.add(pizza)
    db.session.commit()
    print("DB seeded!")

@app.route('/')
def home():
    return "API works"'' \

@app.route('/users')
def users():
    users = User.query.all()
    result = users_schema.dump(users)
    if result:
        return jsonify(result)
    else:
        return "No users"

@app.route('/login', methods = ['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    if User.query.filter_by(email = email , password = password).first():
        access_token = create_access_token(identity=email)
        return jsonify(message = "login successful", access_token = access_token)
    else:
        return jsonify(message = "ID or Password doesn not match") , 401

@app.route('/dishes')
def dishes():
    dishes = Dish.query.all()
    result = dishes_schema.dump(dishes)
    return  jsonify(data = result)

@app.route('/dish/<int:id>')
def dish(id : int):
    dish = Dish.query.filter_by(id = id).first()
    result = dish_schema.dump(dish)
    return jsonify(data = result)

@app.route('/register', methods = ['POST'])
def register():
    email = request.form['email']
    is_existing_email = User.query.filter_by(email=email).first()

    if is_existing_email:
        return jsonify(message = "User already exists"), 409
    else:
        name = request.form['name']
        password = request.form['password']
        user = User(name = name , email = email , password = password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message = "User created successfully!")

@app.route('/add_rating/<int:id>',methods = ['POST'])
def add_rating(id:int):
    dish = Dish.query.filter_by(id=id).first()
    if dish:
        dish_obj = dish_schema.dump(dish)
        current_rating = dish_obj['rating']
        number_of_reviews = dish_obj['number_of_reviews']
        print('Existing Rating is: '+str(current_rating))
        new_rating = ((current_rating * number_of_reviews) + request.json['rating']) / (number_of_reviews + 1)
        dish.rating = new_rating
        dish.number_of_reviews = number_of_reviews + 1
        db.session.commit()
        return jsonify(message = "Rating has been successfully updated")
    else:
        return jsonify(message = "Dish not found") , 404

@app.route('/add_dish', methods = ['POST'])
@jwt_required()
def add_dish():
    new_dish_name = request.form['name'].lower()
    is_existing = Dish.query.filter_by(name = new_dish_name).first()
    if is_existing:
        return jsonify(message = 'Already exists') , 409
    else:
        price = request.form['price']
        new_dish = Dish(name = new_dish_name,price = price , rating = 5 , number_of_reviews = 1)
        db.session.add(new_dish)
        db.session.commit()
        return jsonify(message = "New dish added successfully")

# Database models
class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)


class Dish(db.Model):
    __tablename__ = "dishes"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    price = Column(Float)
    rating = Column(Float)
    number_of_reviews = Column(Integer)


# Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password')


class DishSchema(ma.Schema):
    class Meta:
        fields = ('id','name', 'price', 'rating', 'number_of_reviews')


user_schema = UserSchema()
dish_schema = DishSchema()

users_schema = UserSchema(many=True)
dishes_schema = DishSchema(many = True)

if __name__ == "__main__":
    app.run()
