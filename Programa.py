from flask import Flask
from flask import render_template

app = Flask("CodeFlix")

@app.route('/home')
def home():
    return  render_template('home.html')

def cadastro():
    return 'cadastro usuarios'
@app.route('/novo')
def cadastrarUsuario():
    return render_template('novo_cadastro.html')
@app.route('/listar')
def listar():
    return render_template('lista.html')
if __name__=='__main__':    
    app.run('0.0.0.0',debug=True, port=8080)
