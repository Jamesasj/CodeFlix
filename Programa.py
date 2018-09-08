from flask import Flask
app = Flask("CodeFlix")

if __name__=='__main__':    
    app.run('0.0.0.0',debug=True, port=80)

@app.route('/')
def home():
    return  'ola mundo!'


def cadastro():
    return 'cadastro usuarios'