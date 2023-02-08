import json


def get_json_data(file_name: str) -> list:
    """Чтение .json файла и возвращение списка со словарями"""
    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data


def add_users_data(class_name) -> list:
    """Добавление пользователей в список для последующего добавления в базу данных"""
    users_list = []
    for user in get_json_data("data/users.json"):
        user_to_add = class_name(
            id=user["id"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            age=user["age"],
            email=user["email"],
            role=user["role"],
            phone=user["phone"]
        )
        users_list.append(user_to_add)
    return users_list


def add_orders_data(class_name) -> list:
    """Добавление заказов в список для последующего добавления в базу данных"""
    orders_list = []
    for order in get_json_data("data/orders.json"):
        order_to_add = class_name(
            id=order["id"],
            name=order["name"],
            description=order["description"],
            start_date=order["start_date"],
            end_date=order["end_date"],
            address=order["address"],
            price=order["price"],
            customer_id=order["customer_id"],
            executor_id=order["executor_id"]
        )
        orders_list.append(order_to_add)
    return orders_list


def add_offers_data(class_name) -> list:
    """Добавление предложений в список для последующего добавления в базу данных"""
    offers_list = []
    for offer in get_json_data("data/offers.json"):
        offer_to_add = class_name(
            id=offer["id"],
            order_id=offer["order_id"],
            executor_id=offer["executor_id"]
        )
        offers_list.append(offer_to_add)
    return offers_list


def add_new_user(class_name, data):
    """Добавление нового пользователя в базу данных"""
    new_user = class_name(
        id=data["id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        age=data["age"],
        email=data["email"],
        role=data["role"],
        phone=data["phone"]
    )
    return new_user


def add_new_order(class_name, data):
    """Добавление нового заказа в базу данных"""
    new_order = class_name(
        id=data["id"],
        name=data["name"],
        description=data["description"],
        start_date=data["start_date"],
        end_date=data["end_date"],
        address=data["address"],
        price=data["price"],
        customer_id=data["customer_id"],
        executor_id=data["executor_id"]
    )
    return new_order


def add_new_offer(classname, data):
    """Добавление нового предложения в базу данных"""
    new_offer = classname(
        id=data["id"],
        order_id=data["order_id"],
        executor_id=data["executor_id"],
    )
    return new_offer
