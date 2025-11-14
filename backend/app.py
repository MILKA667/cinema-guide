from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2 import DatabaseError
import jwt
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'feojsngfuimnco4itui4' 

CORS(app)


def get_current_user():
    auth_header = request.headers.get('Authorization')
    print("Authorization header:", auth_header)
    if not auth_header:
        return None
    
    try:
        parts = auth_header.split(" ")
        if len(parts) == 2 and parts[0] == "Bearer":
            token = parts[1]
        else:
            token = auth_header 
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        print("Decoded payload:", payload)
        return payload['user_id']
    except Exception as e:
        print("JWT decode error:", e)
        return None



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
            print('dasdads')
            token = jwt.encode({
                'user_id': user[0],
                'email': email,
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            if isinstance(token, bytes):
                token = token.decode('utf-8')
                
            return jsonify({
                'message': 'Login successful',
                'token': token,
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
        print(e)
        return jsonify({'error': 'Server error: ' + str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.route('/api/movies', methods=['GET'])
def get_movies():
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT id, title, poster_url FROM movies ORDER BY rating DESC LIMIT 100;")
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


@app.route('/api/watch_movie', methods=['POST'])
def watch_movie():
    data = request.get_json()
    movie_id = data.get('movie_id')
    
    user_id = get_current_user()
    if not user_id:
        return jsonify({'error': 'Не авторизовано'}), 401

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO user_watched (user_id, movie_id, watched_at) VALUES (%s, %s, NOW()) ON CONFLICT (user_id, movie_id) DO NOTHING;",
            (user_id, movie_id)
        )
        conn.commit()
        return jsonify({'message': 'Просмотренно'}), 200
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    user_id = get_current_user()
    if not user_id:
        return jsonify({'error': 'Не авторизовано'}), 401

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
        WITH top_genres AS (
            SELECT m.genre_id, COUNT(*) AS cnt
            FROM movies m
            JOIN user_watched uw ON m.id = uw.movie_id
            WHERE uw.user_id = %s
            GROUP BY m.genre_id
            ORDER BY cnt DESC
            LIMIT 3
        ),
        top_directors AS (
            SELECT m.director_id, COUNT(*) AS cnt
            FROM movies m
            JOIN user_watched uw ON m.id = uw.movie_id
            WHERE uw.user_id = %s
            GROUP BY m.director_id
            ORDER BY cnt DESC
            LIMIT 3
        )
        SELECT m.id, m.title, m.rating, m.poster_url,
               CASE WHEN m.genre_id IN (SELECT genre_id FROM top_genres) THEN 1 ELSE 0 END +
               CASE WHEN m.director_id IN (SELECT director_id FROM top_directors) THEN 1 ELSE 0 END AS score
        FROM movies m
        WHERE m.id NOT IN (
            SELECT movie_id FROM user_watched WHERE user_id = %s
        )
        ORDER BY score DESC, m.rating DESC
        LIMIT 5;
        """, (user_id, user_id, user_id))

        rows = cur.fetchall()
        recommendations = [
            {"id": r[0], "title": r[1], "rating": float(r[2]), "poster_url": r[3]} 
            for r in rows
        ]
        return jsonify(recommendations), 200

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

