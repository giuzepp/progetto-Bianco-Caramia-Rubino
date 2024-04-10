from flask import Flask, render_template, redirect, request, session, url_for
import sqlite3
import string
import random

app = Flask(__name__)

# Funzione per creare la SECRET_KEY
def generate_random_string(length):
    # Define the characters you want to include in the random string
    characters = string.ascii_letters + string.digits + string.punctuation
    # Generate the random string by selecting characters randomly
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

random_string = generate_random_string(50)
app.config['SECRET_KEY'] = random_string

@app.route('/')
def template():
    return render_template('template.html')

# Esegue la home
@app.route('/home')
def index():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection.close()
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/contatti')
def contatti():
    return render_template('contatti.html')

# Esegue il login
@app.route('/executelogin', methods=('POST',))
def executelogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        query = 'SELECT CFU, email, password FROM UTENTE where email="' + email + '" and password="' + password + '"'
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row
        result = connection.execute(query).fetchall()

        for row in result:
            A = row['CFU']

        if len(result) == 0:
            print("Credenziali non corrette")
            return render_template('template.html')
        else:
            print("Logged in")
            session["connesso"] = True
            session["nome"] = email
            session["CFU"] = A
            session.modified = True
            print("sessione:", session["nome"])
            return redirect(url_for('logok'))
    return render_template('template.html')

@app.route('/logok', methods=['GET'])
def logok():
    utente = session.get("CFU")
    print(utente)
    print(session.get("nome", None))
    if not session.get("nome"):
        return render_template('template.html')
    return render_template('index.html', utente=utente)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Esegue la registrazione
@app.route('/executesignup', methods=('POST',))
def executesignup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection.execute('INSERT INTO UTENTE(CFU, email, password) VALUES(?, ?, ?)', (username, email, password))
    connection.commit()
    connection.close()
    return redirect('/')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80)
