from flask import Flask, render_template, redirect, request, session
import sqlite3

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    connection = sqlite3.connect('database.db')
    connection.row_factory=sqlite3.Row
    connection.close()
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

#esegue il login
@app.route('/executelogin', methods=('POST',))
def executelogin():
    email = request.form['email']
    password = request.form['password']
    #print(email, password)
    query = 'SELECT CFU, email, password FROM utenti where email="' + email + '" and password="' + password + '"'
    #print(query)
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    result = connection.execute(query).fetchall()

##############################################################################
    if (len(result)) == 0:
        print("Credenziali non corrette")
        return render_template('login.html')
    else:
        print("Logged in")
        session["nome"] = user
        session["connesso"] = True
        session.modified = True
        print("sessione:", session["nome"])
        return redirect(url_for('logok'))
###############################################################################

#esegue la registrazione
@app.route('/executesignup', methods=('POST',))
def executesignup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    #print(username, email, password)
    connection = sqlite3.connect('database.db')
    connection.row_factory=sqlite3.Row
    connection.execute('INSERT INTO UTENTE(CFU, email, password) VALUES(?, ?, ?)', (username, email, password))
    connection.commit()
    connection.close()
    return redirect('/')


app.run(host='127.0.0.1', port=80)