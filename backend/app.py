from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2 import DatabaseError
import os
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'feojsngfuimnco4itui4' 

CORS(app)

def get_db_connection():
    return psycopg2.connect(
        dbname='cinema_guide',
        user='editor',
        password='qwer1234',
        host='185.237.95.6'
    )

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/api/register', methods=['POST'])
def register():  
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({'error': 'Такой пользователь уже существует'}), 409
        
        cur.execute(
            "INSERT INTO users (email, password) VALUES (%s, %s)",
            (email, password)
        )
        conn.commit()
        return jsonify({"message": "Регистрация успешна!"}), 201
        
    except DatabaseError as e:
        if conn:
            conn.rollback()
        return jsonify({'error': 'Database error: ' + str(e)}), 400
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'error': 'Server error: ' + str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    
    data = request.get_json()  
    email = data['email']
    password = data['password']

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone() 
        
        if user and user[1] == password:
            token = jwt.encode({
                'user_id': user[0],
                'email': email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            if isinstance(token, bytes):
                token = token.decode('utf-8')
                
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user_id': user[0]
            }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
        
    except DatabaseError as e:
        if conn:
            conn.rollback()
        return jsonify({'error': 'Database error: ' + str(e)}), 400
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'error': 'Server error: ' + str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.route('/api/recomendation', methods=['GET'])
def get_movies():
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT id, title, poster_url FROM movies ORDER BY rating DESC LIMIT 5;")
        rows = cur.fetchall()

        movies = []
        for row in rows:
            movies.append({
                "id": row[0],
                "title": row[1],
                "poster_url": row[2]
            })

        return jsonify(movies), 200
        
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()        


if __name__ == '__main__':
    app.run(debug=True, port=5000)

