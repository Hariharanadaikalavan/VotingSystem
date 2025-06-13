from flask import Flask, request, jsonify
from db import get_connection
from flask_cors import CORS
from flask_bcrypt import Bcrypt



app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

@app.route('/candidates', methods=['GET'])
def get_candidates():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM candidates")
    result = cursor.fetchall()
    conn.close()
    return jsonify(result)

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    candidate_id = data['candidate_id']
    user_id = data['user_id']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT has_voted FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "User not found"})

    if user['has_voted']:
        return jsonify({"error": "You have already voted"})

    cursor.execute("UPDATE candidates SET votes = votes + 1 WHERE id = %s", (candidate_id,))
    cursor.execute("UPDATE users SET has_voted = TRUE WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Vote submitted successfully"})


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name']
    email = data['email']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                       (name, email, password))
        conn.commit()
        return jsonify({"message": "User registered successfully"})
    except:
        return jsonify({"error": "User already exists"})
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful", "user_id": user['id'], "has_voted": user['has_voted']})
    else:
        return jsonify({"error": "Invalid email or password"})


if __name__ == '__main__':
    app.run(debug=True)
