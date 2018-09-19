from flask import Flask, redirect, url_for, request,render_template, abort,jsonify
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
    with open('dados/filmes/data.json') as f:
        data = json.load(f)
    return render_template('lista.html', folder = folder)

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

@app.route('/obterFilmes', methods=['POST'])
def obterFilmes():
    with open('dados/' + request.form['folder'] + '/data.json') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/avaliar/<pasta>/<filme>/<nota>')
def avaliar(pasta, filme, nota):
    nm_arquivo =  "dados/modelo/data.json"
    classifi = {filme : nota}
    listaPastas = list()

    if os.path.exists(nm_arquivo):
        with open( nm_arquivo ,'r+') as arquivo:
            listaPastas = json.load(arquivo)  
    novoItem = {pasta : {filme : nota}}
    listaPastas.append(novoItem)
    
    with open( nm_arquivo ,'w+') as arquivo:
        json.dump(listaPastas , arquivo)

    with open("dados/" + pasta +"/data.json",'r' ) as arquivo:
        listaFilmes = json.load(arquivo)
    
    for i, item in enumerate(listaFilmes["filmes"]):
        if(item['id'] == filme):
            listaFilmes['filmes'].pop(i)
            break

    with open("dados/" + pasta +"/data.json",'w' ) as arquivo:
        json.dump(listaFilmes , arquivo)
        
    return redirect(url_for("listar",folder = pasta))


if __name__=='__main__':    
    app.run('0.0.0.0',debug=True, port=8080)
