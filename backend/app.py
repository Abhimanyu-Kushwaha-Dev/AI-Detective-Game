import os
import sys
import random
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add parent directory to paths so Python can find main.py cleanly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from main import generate_game_content
except ImportError:
    print("Error: Could not import generate_game_content from main.py. Ensure main.py is in the parent directory.")

app = Flask(__name__)
# Enable CORS for frontend integration
CORS(app)

@app.route('/api/new-game', methods=['GET'])
def new_game():
    """Starts a new case, fetches AI data, and selects the culprit."""
    game_data = generate_game_content()
    
    if not game_data:
        return jsonify({"error": "Failed to generate game content from Gemini"}), 500
        
    # Inject unique structural IDs onto suspects for easy frontend tracking
    for idx, suspect in enumerate(game_data.get('suspects', []), 1):
        suspect['id'] = idx
        
    # Pick the thief at random
    thief_index = random.randint(0, len(game_data['suspects']) - 1)
    thief_id = game_data['suspects'][thief_index]['id']
    
    return jsonify({
        "victim": game_data['victim'],
        "suspects": game_data['suspects'],
        "thief_id": thief_id
    })


@app.route('/api/verify-accusation', methods=['POST'])
def verify_accusation():
    """Validates an accusation option submitted by the frontend player."""
    data = request.json or {}
    accused_id = data.get('accused_id')
    thief_id = data.get('thief_id')
    
    if not accused_id or not thief_id:
        return jsonify({"error": "Missing accused_id or thief_id data parameter"}), 400
        
    if accused_id == thief_id:
        return jsonify({
            "correct": True,
            "message": "CORRECT! Magnificent detective work, you caught the thief red-handed!",
            "bonus_points": 100
        })
    else:
        return jsonify({
            "correct": False,
            "message": "WRONG! That suspect's defense holds up under pressure. Keep digging!",
            "bonus_points": 0
        })


if __name__ == '__main__':
    app.run(debug=True, port=5000)