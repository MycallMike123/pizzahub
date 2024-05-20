from flask import Flask, jsonify, request, abort
from flaskpizza.models import Restaurant, Pizza, RestaurantPizza, db
from flaskpizza import app



# Route handler for GET /restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    # Retrieve all restaurants from the database
    restaurants = Restaurant.query.all()
    
    # Create a list to store the restaurant data
    restaurant_list = []
    
    # Iterate through the restaurants and create a dictionary for each restaurant
    for restaurant in restaurants:
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address
        }
        restaurant_list.append(restaurant_data)
    
    # Return the restaurant data as JSON
    return jsonify(restaurant_list)


# Route handler for GET /restaurants/:id
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    # Retrieve the restaurant by its ID from the database
    restaurant = Restaurant.query.get(id)
    
   # Check if the restaurant exists
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404
    
    # Create a dictionary for the restaurant data
    restaurant_data = {
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address
    }
    
    # Return the restaurant data as JSON
    return jsonify(restaurant_data)

# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Restaurant not found'}), 404




# Route handler for DELETE /restaurants/:id
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    # Retrieve the restaurant by its ID from the database
    restaurant = Restaurant.query.get(id)
    
    # Check if the restaurant exists
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404
    
    # Delete the associated RestaurantPizza entries
    RestaurantPizza.query.filter_by(restaurant_id=id).delete()
    
    # Delete the restaurant
    db.session.delete(restaurant)
    db.session.commit()
    
    # Return an empty response body
    return '', 204


# Route handler for GET /pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    # Retrieve all pizzas from the database
    pizzas = Pizza.query.all()
    
    # Create a list to store the pizza data
    pizza_list = []
    
    # Iterate over the pizzas and create a dictionary for each pizza
    for pizza in pizzas:
        pizza_data = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }
        pizza_list.append(pizza_data)
    
    # Return the pizza data as JSON
    return jsonify(pizza_list)


# Route handler for POST /restaurant_pizzas
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    # Get the request data
    data = request.json
    
    # Extract the properties from the request data
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')
    
    # Validate the required properties
    if not price or not pizza_id or not restaurant_id:
        return jsonify({'errors': ['validation errors']}), 400
    
    # Check if the Pizza and Restaurant exist
    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)
    
    if not pizza or not restaurant:
        return jsonify({'errors': ['validation errors']}), 400
    
    # Create a new RestaurantPizza
    restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
    db.session.add(restaurant_pizza)
    db.session.commit()
    
    # Return the pizza data related to the created RestaurantPizza
    pizza_data = {
        'id': pizza.id,
        'name': pizza.name,
        'ingredients': pizza.ingredients
    }
    
    return jsonify(pizza_data), 201
