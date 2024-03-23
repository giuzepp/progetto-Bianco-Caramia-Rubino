from flask import Flask, render_template 

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')
def catalogo():
    return render_template('catalogo.html')

app.run(host='0.0.0.0', port=80)