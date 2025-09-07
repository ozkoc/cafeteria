from flask import Flask, request, jsonify

app = Flask(__name__)

# Example in-memory "database"
items = {
    1: "data", 
    2: 1980, 
    3: True }

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items), 200

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = items.get(item_id, None)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Invalid data"}), 400
    item = {"id": len(items) + 1, "name": data['name']}
    items.append(item)
    return jsonify(item), 201



@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    item = next((i for i in items if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    item["name"] = data.get("name", item["name"])
    return jsonify(item), 200

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [i for i in items if i["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
