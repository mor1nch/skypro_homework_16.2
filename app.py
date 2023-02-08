from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from utils import *
import json
import logging

logging.basicConfig(filename="log.log", level=logging.DEBUG, filemode="w",
                    format="%(asctime)s [%(levelname)s] %(message)s")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db: SQLAlchemy = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.Integer)

    def instance_to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    customer = db.relationship("User", foreign_keys=[customer_id])
    executor = db.relationship("User", foreign_keys=[executor_id])

    def instance_to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    customer = db.relationship("User")
    executor = db.relationship("Order")

    def instance_to_dict(self) -> dict:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


with app.app_context():
    db.create_all()

    user = add_users_data(User)
    db.session.add_all(user)
    db.session.commit()

    order = add_orders_data(Order)
    db.session.add_all(order)
    db.session.commit()

    offer = add_offers_data(Offer)
    db.session.add_all(offer)
    db.session.commit()


@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        result = []
        all_users = User.query.all()
        for user_ in all_users:
            result.append(user_.instance_to_dict())
        logging.info("GET Запрос по адресу http://127.0.0.1:5000/users")
        return jsonify(result)

    elif request.method == 'POST':
        user_data = json.loads(request.data)
        modified_user = add_new_user(User, user_data)
        db.session.add(modified_user)
        db.session.commit()
        logging.info("POST Запрос по адресу http://127.0.0.1:5000/users")
        return 'Все гуд, обновление внесено в базу данных', 201


@app.route('/users/<uid>', methods=['GET', 'PUT', 'DELETE'])
def get_user_by_id(uid):
    if request.method == 'GET':
        user_by_id = User.query.get(uid)
        logging.info("GET Запрос по адресу http://127.0.0.1:5000/users/<uid>")
        return jsonify(user_by_id.instance_to_dict())

    elif request.method == 'PUT':
        data_to_update = json.loads(request.data)
        user_by_id = User.query.get(uid)

        user_by_id.id = data_to_update['id']
        user_by_id.first_name = data_to_update["first_name"]
        user_by_id.last_name = data_to_update["last_name"]
        user_by_id.age = data_to_update['age']
        user_by_id.email = data_to_update['email']
        user_by_id.role = data_to_update['role']
        user_by_id.phone = data_to_update['phone']

        db.session.add(user_by_id)
        db.session.commit()
        logging.info("PUT Запрос по адресу http://127.0.0.1:5000/users/<uid>")
        return 'Все гуд, обновление внесено в базу данных', 201

    elif request.method == 'DELETE':
        user_to_delete = User.query.get(uid)
        db.session.delete(user_to_delete)
        db.session.commit()
        logging.info("DELETE Запрос по адресу http://127.0.0.1:5000/users/<uid>")
        return 'Все гуд, обновление внесено в базу данных', 201


@app.route('/orders', methods=['GET', 'POST'])
def get_order():
    if request.method == 'GET':
        result = []
        orders_to_show = Order.query.all()
        for orders in orders_to_show:
            result.append(orders.instance_to_dict())
        logging.info("GET Запрос по адресу http://127.0.0.1:5000/orders")
        return jsonify(result)

    elif request.method == 'POST':
        order_data = json.loads(request.data)
        modified_order = add_new_order(Order, order_data)
        db.session.add(modified_order)
        db.session.commit()
        logging.info("POST Запрос по адресу http://127.0.0.1:5000/orders")
        return 'Все гуд, обновление внесено в базу данных', 201


@app.route('/orders/<uid>', methods=['GET', 'PUT', 'DELETE'])
def get_order_by_id(uid):
    if request.method == 'GET':
        order_by_id = Order.query.get(uid)
        logging.info("GET Запрос по адресу http://127.0.0.1:5000/orders/<uid>")
        return jsonify(order_by_id.instance_to_dict())

    elif request.method == 'PUT':
        data_to_update = json.loads(request.data)
        order_by_id = Order.query.get(uid)

        order_by_id.id = data_to_update['id']
        order_by_id.name = data_to_update["name"]
        order_by_id.description = data_to_update["description"]
        order_by_id.start_date = data_to_update['start_date']
        order_by_id.end_date = data_to_update['end_date']
        order_by_id.address = data_to_update['address']
        order_by_id.price = data_to_update['price']
        order_by_id.customer_id = data_to_update['customer_id']
        order_by_id.executor_id = data_to_update['executor_id']

        db.session.add(order)
        db.session.commit()
        logging.info("PUT Запрос по адресу http://127.0.0.1:5000/orders/<uid>")
        return 'Все гуд, обновление внесено в базу данных', 201

    elif request.method == 'DELETE':
        order_by_id = Order.query.get(uid)
        db.session.delete(order_by_id)
        db.session.commit()
        logging.info("DELETE Запрос по адресу http://127.0.0.1:5000/orders/<uid>")
        return 'Все гуд, обновление внесено в базу данных', 201


@app.route('/offers', methods=['GET', 'POST'])
def get_offers():
    if request.method == 'GET':
        result = []
        all_offers = Offer.query.all()
        for offer_ in all_offers:
            result.append(offer_.instance_to_dict())
        logging.info("GET Запрос по адресу http://127.0.0.1:5000/offers")
        return jsonify(result)

    elif request.method == 'POST':
        offer_data = json.loads(request.data)
        modified_offer = add_new_offer(Offer, offer_data)
        db.session.add(modified_offer)
        db.session.commit()
        logging.info("POST Запрос по адресу http://127.0.0.1:5000/offers")
        return 'Все гуд, обновление внесено в базу данных', 201


@app.route('/offers/<uid>', methods=['GET', 'PUT', 'DELETE'])
def get_offer_by_id(uid):
    if request.method == 'GET':
        offer_by_id = Offer.query.get(uid)
        logging.info("GET Запрос по адресу http://127.0.0.1:5000/offers/<uid>")
        return jsonify(offer_by_id.instance_to_dict())

    elif request.method == 'PUT':
        data_to_update = json.loads(request.data)
        offer_by_id = Offer.query.get(uid)

        offer_by_id.id = data_to_update['id']
        offer_by_id.order_id = data_to_update["order_id"]
        offer_by_id.executor_id = data_to_update["executor_id"]

        db.session.add(offer_by_id)
        db.session.commit()
        logging.info("PUT Запрос по адресу http://127.0.0.1:5000/offers/<uid>")
        return 'Все гуд, обновление внесено в базу данных', 201

    elif request.method == 'DELETE':
        offer_by_id = Offer.query.get(uid)
        db.session.delete(offer_by_id)
        db.session.commit()
        logging.info("DELETE Запрос по адресу http://127.0.0.1:5000/offers/<uid>")
        return 'Все гуд, обновление внесено в базу данных', 201


if __name__ == '__main__':
    app.run()
