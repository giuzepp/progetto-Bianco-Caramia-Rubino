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
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    query = 'SELECT IDL, titolo, lingua, genere, anno_pubblicazione, anno_edizione, cognome, n_pag FROM LIRBO INNER JOIN AUTORE ON LIRBO.CFA = AUTORE.CFA'
    result = connection.execute(query).fetchall()
    #print(result)
    return render_template('catalogo.html', result=result)


@app.route('/info')
def info():
    return render_template('info.html')

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
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    query = 'SELECT * FROM UTENTE WHERE CFU="' + utente + '"'
    result = connection.execute(query).fetchall()

    #presa dei dati dal database
    for row in result:
        nome = row['nome']
        cognome = row['cognome']
        eta = row['eta']
        telefono = row['telefono']
        via = row['via']
        cap = row['cap']
        citta = row['citta']

    print("citta:", citta)
    #print(utente)
    print(session.get("nome", None))
    if not session.get("nome"):
        return render_template('template.html')
    return render_template('index.html', utente=utente, nome=nome, cognome=cognome, eta=eta, telefono=telefono, via=via, cap=cap, citta=citta)
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

@app.route('/registrazioneanagrafica', methods=('POST','GET'))
def registrazioneanagrafica():
    utente = session.get("CFU")
    print("prova", utente)
    #presi dal form
    nome = request.form['nome']
    cognome = request.form['cognome']
    eta = request.form['eta']
    telefono = request.form['telefono']
    via = request.form['via']
    cap = request.form['cap']
    citta = request.form['citta']

    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    
    # Verifica se il CFU esiste nella tabella
    cfu_row = connection.execute('SELECT * FROM UTENTE WHERE CFU = ?', (utente,)).fetchone()

    if cfu_row:
        # Se il CFU esiste, esegui l'inserimento nella riga specifica
        connection.execute('UPDATE UTENTE SET nome=?, cognome=?, eta=?, telefono=?, via=?, cap=?, citta=? WHERE CFU=?',
                        (nome, cognome, eta, telefono, via, cap, citta, utente))
        connection.commit()
        connection.close()
        return redirect(url_for('logok', nome=nome, cognome=cognome, eta=eta, telefono=telefono, via=via, cap=cap, citta=citta))
    else:
        # Se il CFU non esiste, gestisci l'errore o fai altro
        connection.close()
        return "CFU non trovato"
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80)
