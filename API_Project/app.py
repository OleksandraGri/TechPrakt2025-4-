from flask import Flask, request, jsonify

app = Flask(__name__)

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
