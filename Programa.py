from flask import Flask, redirect, url_for, request,render_template, abort
import os, json

app = Flask("CodeFlix")

@app.route('/home')
def home():
    return  render_template('home.html')

def cadastro():
    return 'cadastro usuarios'

@app.route('/novo')
def cadastrarUsuario():
    return render_template('novo_cadastro.html')

@app.route('/listar/<folder>')
def listar(folder):
    print(folder)
    return render_template('lista.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nomePasta = "dados/"+ request.form['senha'] + request.form['usuario']
    if not os.path.exists(nomePasta):
        os.makedirs(nomePasta)
    nome = request.form['nome']
    sobrenome = request.form['sobrenome']
    with open(nomePasta + "\\user.json",'w') as arquivo:
        json.dump({"nome" : nome, "sobrenome" : sobrenome } , arquivo)
    return redirect(url_for("home"))

@app.route('/logar', methods=['POST'])
def logar():
    nomePasta = "dados/"+ request.form['senha'] + request.form['usuario']
    if os.path.exists(nomePasta):
        return "/listar/"+ request.form['senha'] + request.form['usuario']
    else:
        return abort(403)

if __name__=='__main__':    
    app.run('0.0.0.0',debug=True, port=8080)
