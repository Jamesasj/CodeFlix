import json

def executar():
    with open("dados/modelo/data.json", 'r') as arquivo:
        treino = json.load(arquivo)
    dicio = dict()
    for item in treino:   
        if item['usuario'] in dicio:
            dicio[item['usuario']].update({item['filme'] : item['nota']})
        else:
            dicio[item['usuario']]={item['filme'] : item['nota']}
    
    print(dicio)

executar()