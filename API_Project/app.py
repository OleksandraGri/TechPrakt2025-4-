from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your_secret_key"
jwt = JWTManager(app)


# Логіка для входу користувача
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Перевірка даних користувача
    if username == "admin" and password == "password":
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    return jsonify({"message": "Bad credentials"}), 401


@app.route('/admin', methods=['GET'])
@jwt_required()
def admin_only():
    current_user = get_jwt_identity()
    if current_user != "admin":
        return jsonify({"message": "Admin access required"}), 403
    return jsonify(message="Welcome Admin!")


@app.route('/user', methods=['GET'])
@jwt_required()
def user_only():
    current_user = get_jwt_identity()
    return jsonify(message=f"Hello {current_user}!")


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# Тимчасова база даних (список)
items = []


@app.route('/')
def home():
    return jsonify({"message": "Welcome to the API!"})


# Створення (Create)
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    item_id = len(items) + 1
    data["id"] = item_id
    items.append(data)
    return jsonify({"message": "Item created", "item": data}), 201


# Отримання всіх елементів (Read)
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)


# Отримання одного елемента (Read)
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in items if i["id"] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"message": "Item not found"}), 404


# Оновлення (Update)
@app.route('/items/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    data = request.json
    item = next((i for i in items if i["id"] == item_id), None)
    if item:
        item.update(data)
        return jsonify({"message": "Item updated", "item": item})
    return jsonify({"message": "Item not found"}), 404


# Видалення (Delete)
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [i for i in items if i["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True)
