from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return  'ola mundo!'


def cadastro():
    return 'cadastro usuarios'