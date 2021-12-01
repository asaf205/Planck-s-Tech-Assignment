from flask import Flask, request, abort, make_response, render_template, redirect
import json
import requests
import threading

app = Flask(__name__)

url = "https://www.10bis.co.il/NextApi/GetRestaurantMenu?culture=en&uiCulture=en&restaurantId=19156&deliveryMethod=pickup"

params = {
    "culture": "en",
    "uiCulture": "en",
    "restaurantId": "19156",
    "deliveryMethod": "pickup"
}


def get_arcaffe_menu():
    arcaffe_menu_json = requests.get(url, params=params).json()
    threading.Timer(600, get_arcaffe_menu).start()
    return arcaffe_menu_json


arcaffe_menu_json = get_arcaffe_menu()


@app.route('/drinks', methods=['GET'])
def get_all_drinks():
    drink_data_from_api = [x for x in arcaffe_menu_json['Data']['categoriesList'] if x['categoryName'] == 'Drinks'][0][
        'dishList']
    header = ['drink_id', 'drink_name', 'drink_description', 'drink_price']
    drink_list = []
    for drink in drink_data_from_api:
        dishId = drink['dishId']
        dishName = drink['dishName']
        dishDescription = drink['dishDescription']
        dishPrice = int(drink['dishPrice'])
        drink_list.append(dict(zip(header, (dishId, dishName, dishDescription, dishPrice))))

    return json.dumps(drink_list)


@app.route('/drink/<int:id>', methods=['GET'])
def get_drink_by_id(id):
    drink_data_from_api = [x for x in arcaffe_menu_json['Data']['categoriesList'] if x['categoryName'] == 'Drinks'][0][
        'dishList']
    header = ['drink_id', 'drink_name', 'drink_description', 'drink_price']
    response = {}  # if the id does not exist
    for drink in drink_data_from_api:
        if drink['dishId'] == int(id):
            dishId = drink['dishId']
            dishName = drink['dishName']
            dishDescription = drink['dishDescription']
            dishPrice = drink['dishPrice']
            response = dict(zip(header, (dishId, dishName, dishDescription, dishPrice)))
            break
    return response


@app.route('/pizzas', methods=['GET'])
def get_all_pizzas():
    pizzas_data_from_api = [x for x in arcaffe_menu_json['Data']['categoriesList'] if x['categoryName'] == 'Pizzas'][0][
        'dishList']
    header = ['pizza_id', 'pizza_name', 'pizza_description', 'pizza_price']
    pizzas_list = []
    for pizza in pizzas_data_from_api:
        dishId = pizza['dishId']
        dishName = pizza['dishName']
        dishDescription = pizza['dishDescription']
        dishPrice = int(pizza['dishPrice'])
        pizzas_list.append(dict(zip(header, (dishId, dishName, dishDescription, dishPrice))))

    return json.dumps(pizzas_list)


@app.route('/pizza/<id>', methods=['GET'])
def get_pizza_by_id(id):
    pizzas_data_from_api = [x for x in arcaffe_menu_json['Data']['categoriesList'] if x['categoryName'] == 'Pizzas'][0][
        'dishList']
    header = ['pizza_id', 'pizza_name', 'pizza_description', 'pizza_price']
    response = {}  # if the id does not exist
    for pizza in pizzas_data_from_api:
        if pizza['dishId'] == int(id):
            dishId = pizza['dishId']
            dishName = pizza['dishName']
            dishDescription = pizza['dishDescription']
            dishPrice = int(pizza['dishPrice'])
            response = dict(zip(header, (dishId, dishName, dishDescription, dishPrice)))
            break

    return response


@app.route('/desserts', methods=['GET'])
def get_all_desserts():
    desserts_data_from_api = [x for x in arcaffe_menu_json['Data']['categoriesList'] if x['categoryName'] == 'Desserts'][0]['dishList']
    header = ['dessert_id', 'dessert_name', 'dessert_description', 'dessert_price']
    desserts_list = []
    for dessert in desserts_data_from_api:
        dishId = dessert['dishId']
        dishName = dessert['dishName']
        dishDescription = dessert['dishDescription']
        dishPrice = int(dessert['dishPrice'])
        desserts_list.append(dict(zip(header, (dishId, dishName, dishDescription, dishPrice))))

    return json.dumps(desserts_list)


@app.route('/dessert/<id>', methods=['GET'])
def get_dessert_by_id(id):
    desserts_data_from_api = [x for x in arcaffe_menu_json['Data']['categoriesList'] if x['categoryName'] == 'Desserts'][0]['dishList']
    header = ['dessert_id', 'dessert_name', 'dessert_description', 'dessert_price']
    response = {}  # if the id does not exist
    for dessert in desserts_data_from_api:
        if dessert['dishId'] == int(id):
            dishId = dessert['dishId']
            dishName = dessert['dishName']
            dishDescription = dessert['dishDescription']
            dishPrice = int(dessert['dishPrice'])
            response = dict(zip(header, (dishId, dishName, dishDescription, dishPrice)))
            break

    return response


# POST /order - receives an order and returns its total price.
@app.route('/order', methods=['POST'])
def return_total_price():
    order = request.get_json()
    print(order)
    final_total_price = sum([final_amount_by_category(key, value) for (key,value) in order.items()])
    response = {"price": final_total_price}

    return json.dumps(response)


def final_amount_by_category(category, item_list):
    total_price = 0
    if category == 'drinks':
        total_price = sum([get_drink_by_id(item)['drink_price'] if get_drink_by_id(item) != {} else 0 for item in item_list])
    elif category == 'pizzas':
        total_price = sum([get_pizza_by_id(item)['pizza_price'] if get_pizza_by_id(item) != {} else 0 for item in item_list])
    elif category == 'desserts':
        for item in item_list:
            item_details = get_dessert_by_id(item)
            if item_details != {}:
                total_price += item_details['dessert_price']
            else:
                total_price = 0
    return total_price


if __name__ == '__main__':
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
