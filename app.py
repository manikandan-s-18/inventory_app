from flask import Flask, request, jsonify, render_template, g
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    'host': "localhost",
    'user': "root",
    'password': "mani",
    'database': "inventory_db",
    'ssl_disabled': True  
}


def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(**DB_CONFIG)
        g.cursor = g.db.cursor(dictionary=True)
    return g.db, g.cursor

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/products-page')
def products_page():
    return render_template('products.html')

@app.route('/locations-page')
def locations_page():
    return render_template('locations.html')

@app.route('/movements-page')
def movements_page():
    return render_template('movements.html')

@app.route('/stock-page')
def stock_page():
    return render_template('stock.html')

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    try:
        name = data.get('name')
        description = data.get('description')
        quantity = data.get('quantity')
        location_id = data.get('location_id')

        if not all([name, description, quantity, location_id]):
            return jsonify({'error': 'Missing fields'}), 400

        db, cursor = get_db()

        cursor.execute("INSERT INTO products (name, description) VALUES (%s, %s)", (name, description))
        product_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO stock (product_id, location_id, quantity)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE quantity = quantity + %s
        """, (product_id, location_id, quantity, quantity))

        db.commit()
        return jsonify({'message': 'Product and stock added successfully'}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/products', methods=['GET'])
def get_products():
    try:
        db, cursor = get_db()
        cursor.execute("SELECT id, name,description FROM products")
        return jsonify(cursor.fetchall())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/locations', methods=['POST'])
def add_location():
    data = request.get_json()
    try:
        name = data.get('name')
        if not name:
            return jsonify({'error': 'Location name is required'}), 400

        db, cursor = get_db()
        cursor.execute("INSERT INTO locations (name) VALUES (%s)", (name,))
        db.commit()
        return jsonify({'message': 'Location added successfully'}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/locations', methods=['GET'])
def get_locations():
    try:
        db, cursor = get_db()
        cursor.execute("SELECT id, name FROM locations")
        return jsonify(cursor.fetchall())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/movements', methods=['POST'])
def add_movement():
    data = request.get_json()
    try:
        db, cursor = get_db()
        product_id = data['product_id']
        from_location_id = data.get('from_location_id')
        to_location_id = data.get('to_location_id')
        quantity = data['quantity']

    
        cursor.execute("""
            INSERT INTO movements (product_id, from_location_id, to_location_id, quantity, movement_date)
            VALUES (%s, %s, %s, %s, NOW())
        """, (product_id, from_location_id, to_location_id, quantity))

      
        if from_location_id:
            cursor.execute("""
                UPDATE stock SET quantity = quantity - %s
                WHERE product_id = %s AND location_id = %s
            """, (quantity, product_id, from_location_id))


            cursor.execute("""
                SELECT quantity FROM stock
                WHERE product_id = %s AND location_id = %s
            """, (product_id, from_location_id))
            result = cursor.fetchone()
            if result and result['quantity'] <= 0:
                cursor.execute("""
                    DELETE FROM stock
                    WHERE product_id = %s AND location_id = %s
                """, (product_id, from_location_id))


        if to_location_id:
            cursor.execute("""
                INSERT INTO stock (product_id, location_id, quantity)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE quantity = quantity + %s
            """, (product_id, to_location_id, quantity, quantity))

        cursor.execute("""
            SELECT SUM(quantity) AS total_qty FROM stock
            WHERE product_id = %s
        """, (product_id,))
        total = cursor.fetchone()
        if total and (total['total_qty'] is None or total['total_qty'] <= 0):
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))

        db.commit()
        return jsonify({'message': 'Movement recorded. Stock updated. Product deleted if total quantity is 0.'}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/movements', methods=['GET'])
def get_movements():
    try:
        db, cursor = get_db()
        cursor.execute("""
            SELECT 
                m.id,
                m.quantity,
                m.movement_date,
                p.name AS product_name,
                fl.name AS from_location_name,
                tl.name AS to_location_name
            FROM movements m
            JOIN products p ON m.product_id = p.id
            LEFT JOIN locations fl ON m.from_location_id = fl.id
            JOIN locations tl ON m.to_location_id = tl.id
            ORDER BY m.movement_date DESC
        """)
        return jsonify(cursor.fetchall())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/stock', methods=['GET'])
def get_stock():
    try:
        db, cursor = get_db()
        cursor.execute("""
            SELECT 
                s.product_id, p.name AS product_name,
                s.location_id, l.name AS location_name,
                s.quantity
            FROM stock s
            JOIN products p ON s.product_id = p.id
            JOIN locations l ON s.location_id = l.id
        """)
        return jsonify(cursor.fetchall())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
