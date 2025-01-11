from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database for fertilizers
fertilizers = {}

# Home route
@app.route('/')
def home():
    return "Welcome to the Fertilizer Management System API!"

# REST API Routes

# 1. GET all fertilizers
@app.route('/fertilizers', methods=['GET'])
def get_all_fertilizers():
    return jsonify({"fertilizers": fertilizers}), 200

# 2. GET a specific fertilizer by ID
@app.route('/fertilizers/<int:fertilizer_id>', methods=['GET'])
def get_fertilizer(fertilizer_id):
    fertilizer = fertilizers.get(fertilizer_id)
    if fertilizer:
        return jsonify(fertilizer), 200
    else:
        return jsonify({"message": "Fertilizer not found."}), 404

# 3. POST a new fertilizer
@app.route('/fertilizers', methods=['POST'])
def add_fertilizer():
    data = request.json
    if not data or not all(key in data for key in ("name", "type", "nutrients")):
        return jsonify({"message": "Invalid input."}), 400

    fertilizer_id = max(fertilizers.keys(), default=0) + 1
    fertilizers[fertilizer_id] = {
        "id": fertilizer_id,
        "name": data["name"],
        "type": data["type"],
        "nutrients": data["nutrients"],
        "description": data.get("description", "")
    }
    return jsonify(fertilizers[fertilizer_id]), 201

# 4. PUT to update an existing fertilizer
@app.route('/fertilizers/<int:fertilizer_id>', methods=['PUT'])
def update_fertilizer(fertilizer_id):
    data = request.json
    if fertilizer_id not in fertilizers:
        return jsonify({"message": "Fertilizer not found."}), 404

    if not data:
        return jsonify({"message": "Invalid input."}), 400

    fertilizers[fertilizer_id].update({
        "name": data.get("name", fertilizers[fertilizer_id]["name"]),
        "type": data.get("type", fertilizers[fertilizer_id]["type"]),
        "nutrients": data.get("nutrients", fertilizers[fertilizer_id]["nutrients"]),
        "description": data.get("description", fertilizers[fertilizer_id]["description"])
    })
    return jsonify(fertilizers[fertilizer_id]), 200

# 5. DELETE a fertilizer by ID
@app.route('/fertilizers/<int:fertilizer_id>', methods=['DELETE'])
def delete_fertilizer(fertilizer_id):
    if fertilizer_id in fertilizers:
        del fertilizers[fertilizer_id]
        return jsonify({"message": "Fertilizer deleted successfully."}), 200
    else:
        return jsonify({"message": "Fertilizer not found."}), 404

# 6. INSERT a fertilizer at a specific position
@app.route('/fertilizers/insert/<int:position>', methods=['POST'])
def insert_fertilizer(position):
    data = request.json
    if not data or not all(key in data for key in ("name", "type", "nutrients")):
        return jsonify({"message": "Invalid input."}), 400

    fertilizer_id = max(fertilizers.keys(), default=0) + 1
    new_fertilizer = {
        "id": fertilizer_id,
        "name": data["name"],
        "type": data["type"],
        "nutrients": data["nutrients"],
        "description": data.get("description", "")
    }

    # Convert dictionary to a list of tuples for ordering
    fertilizer_list = list(fertilizers.items())

    if position < 0 or position > len(fertilizer_list):
        return jsonify({"message": "Invalid position."}), 400

    # Insert the new fertilizer
    fertilizer_list.insert(position, (fertilizer_id, new_fertilizer))

    # Convert back to dictionary
    global fertilizers
    fertilizers = dict(fertilizer_list)

    return jsonify(new_fertilizer), 201

if __name__ == '__main__':
    app.run(debug=True)
