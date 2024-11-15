from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database configuration for Flask-MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Assel12.06.2006'
app.config['MYSQL_DB'] = 'art_guide'

# Initialize Flask-MySQL
mysql = MySQL(app)

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']
        
        # Insert the new user into the database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('index'))
    
    return render_template('register.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        cursor = mysql.connection.cursor()
        # Используем правильное имя колонки user_id вместо id
        cursor.execute("SELECT user_id, username, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            if check_password_hash(user[2], password):
                session['user_id'] = user[0]
                session['username'] = user[1]
                return redirect(url_for('index'))
            else:
                return 'Invalid password, try again.'
        else:
            return 'A user with that name was not found.'

    return render_template('login.html')

# Function to save messages to the database using Flask-MySQL
def save_message_to_db(message):
    try:
        cursor = mysql.connection.cursor()  # Get cursor from MySQL connection
        query = "INSERT INTO messages (message) VALUES (%s)"
        cursor.execute(query, (message,))
        mysql.connection.commit()  # Commit the transaction
        print("Message saved successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()  # Close the cursor

# Contact route for displaying and handling the form submission
@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        message = request.form['message']
        save_message_to_db(message)  # Сохраняем сообщение в базу данных
        return redirect(url_for('index'))


@app.route('/')
def index():
    if 'user_id' in session:
        username = session['username']  # Получаем имя пользователя из сессии

        return render_template('index.html', username=username)  # Передаем только username
    return render_template('index.html')  # Если пользователь не авторизован, просто отрисовываем главную страницу


@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Удаляем user_id из сессии
    session.pop('username', None)  # Удаляем username из сессии
    return redirect(url_for('index'))  # Перенаправляем на главную страницу


# Функция для получения соединения с базой данных
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',  # Адрес сервера MySQL
            user='root',  # Имя пользователя MySQL
            password='Assel12.06.2006',  # Пароль пользователя
            database='art_guide'  # Название базы данных
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None
@app.route('/exhibitions', methods=['GET'])
def exhibitions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Запрос к базе данных для получения всех выставок
    cursor.execute("SELECT id, title, date, location, description FROM exhibitions")
    exhibitions_data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(exhibitions_data)

@app.route('/exhibition', methods=['POST'])
def add_exhibition():
    title = request.form.get('title')
    date = request.form.get('date')
    location = request.form.get('location')
    description = request.form.get('description')
    
    if not title or not date:
        return jsonify({"success": False, "message": "Title and date are required!"})
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Вставка новой выставки в таблицу
    cursor.execute(
        "INSERT INTO exhibitions (title, date, location, description) VALUES (%s, %s, %s, %s)", 
        (title, date, location, description)
    )
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return jsonify({"success": True, "message": f"Exhibition '{title}' added successfully!"})

@app.route('/exhibition/<int:exhibition_id>', methods=['GET'])
def exhibition_details(exhibition_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Запрос для получения подробной информации о выставке
    cursor.execute("SELECT * FROM exhibitions WHERE id = %s", (exhibition_id,))
    exhibition = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if exhibition is None:
        return jsonify({"success": False, "message": "Exhibition not found!"})
    
    return jsonify(exhibition)



# Страница для жанра Classicism
@app.route('/classicism')
def classicism():
    return render_template('classicism.html')

@app.route('/impressionism')
def impressionism():
    return render_template('impressionism.html')

@app.route('/romanticism')
def romanticism():
    return render_template('romanticism.html')

@app.route('/realism')
def realism():
    return render_template('realism.html')

@app.route('/surrealism')
def surrealism():
    return render_template('surrealism.html')

@app.route('/baroque')
def baroque():
    return render_template('baroque.html')

@app.route('/expressionism')
def expressionism():
    return render_template('expressionism.html')

@app.route('/fauvism')
def fauvism():
    return render_template('fauvism.html')

@app.route('/art_nouveau')
def art_nouveau():
    return render_template('art_nouveau.html')

@app.route('/constructivism')
def constructivism():
    return render_template('constructivism.html')

@app.route('/pre_raphaelite_brotherhood')
def pre_raphaelite_brotherhood():
    return render_template('pre_raphaelite_brotherhood.html')

@app.route('/abstract_art')
def abstract_art():
    return render_template('abstract_art.html')

@app.route('/van_gogh')
def van_gogh():
    return render_template('van_gogh.html')

@app.route('/dali_salvador')
def dali_salvador():
    return render_template('dali_salvador.html')

@app.route('/da_vinci')
def da_vinci():
    return render_template('da_vinci.html')

@app.route('/michelangelo')
def michelangelo():
    return render_template('michelangelo.html')

@app.route('/raphael')
def raphael():
    return render_template('raphael.html')

@app.route('/caravaggio')
def caravaggio():
    return render_template('caravaggio.html')

@app.route('/rubens')
def rubens():
    return render_template('rubens.html')

@app.route('/rembrandt')
def rembrandt():
    return render_template('rembrandt.html')

@app.route('/monet')
def monet():
    return render_template('monet.html')

@app.route('/manet')
def manet():
    return render_template('manet.html')

@app.route('/renoir')
def renoir():
    return render_template('renoir.html')

@app.route('/monalisa')
def monalisa():
    return render_template('monalisa.html')

@app.route('/starry_night')
def starry_night():
    return render_template('starry_night.html')

@app.route('/guernica')
def guernica():
    return render_template('guernica.html')

@app.route('/last_supperet')
def last_supper():
    return render_template('last_supper.html')

@app.route('/school_of_athens')
def school_of_athens():
    return render_template('school_of_athens.html')

@app.route('/birth_of_venus')
def birth_of_venus():
    return render_template('birth_of_venus.html')

@app.route('/the_night_watch')
def the_night_watch():
    return render_template('the_night_watch.html')

@app.route('/water_lilies')
def water_lilies():
    return render_template('water_lilies.html')

@app.route('/the_scream')
def the_scream():
    return render_template('the_scream.html')

@app.route('/the_persistence_of_memory')
def the_persistence_of_memory():
    return render_template('the_persistence_of_memory.html')

if __name__ == '__main__':
    app.run(debug=True)
