document.addEventListener('DOMContentLoaded', function() {
    const restaurantsList = document.getElementById('restaurants-list');
    const pizzasList = document.getElementById('pizzas-list');
    const addForm = document.getElementById('add-restaurant-pizza-form');

    // Fetch and display restaurants
    fetch('/restaurants')
        .then(response => response.json())
        .then(data => {
            data.forEach(restaurant => {
                const li = document.createElement('li');
                li.textContent = `ID: ${restaurant.id}, Name: ${restaurant.name}, Address: ${restaurant.address}`;
                restaurantsList.appendChild(li);
            });
        });

    // Fetch and display pizzas
    fetch('/pizzas')
        .then(response => response.json())
        .then(data => {
            data.forEach(pizza => {
                const li = document.createElement('li');
                li.textContent = `ID: ${pizza.id}, Name: ${pizza.name}, Ingredients: ${pizza.ingredients}`;
                pizzasList.appendChild(li);
            });
        });

    // Handle form submission
    addForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const restaurantId = document.getElementById('restaurant-id').value;
        const pizzaId = document.getElementById('pizza-id').value;
        const price = document.getElementById('price').value;

        fetch('/restaurant_pizzas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                restaurant_id: restaurantId,
                pizza_id: pizzaId,
                price: price
            })
        })
        .then(response => response.json())
        .then(data => {
            alert('Restaurant Pizza added successfully!');
        })
        .catch(error => {
            alert('Error adding Restaurant Pizza');
            console.error(error);
        });
    });
});
