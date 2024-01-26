from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample product data (replace with your database)
products = [
    {"id": 1, "name": "Product 1", "price": 100},
    {"id": 2, "name": "Product 2", "price": 150},
    {"id": 3, "name": "Product 3", "price": 80},
    {"id": 4, "name": "Product 4", "price": 200},
    {"id": 5, "name": "Product 5", "price": 75},
    # Add more products as needed
]

# Dictionary to store negotiation data
negotiation_data = {}


@app.route('/')
def index():
    return render_template('index.html', products=products)


@app.route('/customer/<int:product_id>', methods=['GET', 'POST'])
def customer(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404

    if request.method == 'POST':
        negotiated_price = float(request.form.get('negotiated_price'))
        negotiation_data[product_id] = {'negotiated_price': negotiated_price, 'status': 'pending'}
        return redirect(url_for('seller', product_id=product_id))

    return render_template('customer.html', product=product)


@app.route('/seller/<int:product_id>', methods=['GET', 'POST'])
def seller(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404

    if request.method == 'POST':
        decision = request.form.get('decision')
        negotiation = negotiation_data.get(product_id)

        if decision == 'accept' and negotiation:
            product['price'] = negotiation['negotiated_price']
            negotiation['status'] = 'accepted'
        elif decision == 'reject' and negotiation:
            # If rejected, reset status to 'pending' for a new negotiation
            negotiation['status'] = 'pending'

        return redirect(url_for('index'))

    return render_template('seller.html', product=product, negotiation=negotiation_data.get(product_id))


@app.route('/handle_decision/<int:product_id>', methods=['POST'])
def handle_decision(product_id):
    decision = request.form.get('decision')
    negotiation = negotiation_data.get(product_id)

    if decision == 'accept' and negotiation:
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            product['price'] = negotiation['negotiated_price']
            negotiation['status'] = 'accepted'
    elif decision == 'reject' and negotiation:
        # If rejected, reset status to 'pending' for a new negotiation
        negotiation['status'] = 'pending'

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
