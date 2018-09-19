import time
import numpy as np
import json
from sklearn.metrics.pairwise import pairwise_distances

def obterBase():
    with open("dados/modelo/data.json", 'r') as arquivo:
        treino = json.load(arquivo)
    
    dicio = dict()
    for item in treino:   
        if item['usuario'] in dicio:
            dicio[item['usuario']].update({item['filme'] : item['nota']})
        else:
            dicio[item['usuario']]={item['filme'] : item['nota']}

    return dicio

def userDict(user="", movie=""):#tag,count=5):
    critics= obterBase()
    if user != "":
        if user in critics:
            return critics[user]
    if movie != "":
        dict_ = {}
        for k in critics.keys():
            if movie in critics[k]:
                dict_[k] = critics[k].get(movie)
            else:
                dict_[k] = 0
        if dict_ != {}:
            return dict_
    return critics

def sim_distance(person1,person2):
    p1, p2, movies= get_vectors(person1, person2)
    p1 = np.array(p1).reshape(1, -1)
    p2 = np.array(p2).reshape(1, -1)
    return 1 - pairwise_distances(p1, p2, metric="cosine")[0][0]

def get_vectors(person1, person2):
    p1 = []
    p2 = []
    movie = []
    for k in person1.keys():
        if k in person2.keys():
            p1.append(person1[k])
            p2.append(person2[k])
            movie.append(k)
    return p1, p2, movie

def best_match(userlist, name1):
    name2 = []
    for p in userlist:
        if p != name1:
            s = sim_distance(userDict(user=name1),userDict(user=p))
            name2.append((p,s))
    return sorted(name2, key=lambda x:x[1])

def recommend(dataset, users, movies, person):
    recommendations = []
    mov_ = [m_ for m_ in movies if m_ not in userDict(user=person)]
    if len(mov_) > 0:
        #Recomendacoes de usuarios com perfil similar.
        for match, sim in best_match(users,  person):
            for midx, m in enumerate(mov_):
                arr = dataset[[uid for uid, u in enumerate(users) if u == match][0]]
                recommendations.append((m, arr[midx]*sim, person, match))
        return sorted(recommendations, key=lambda x:x[1])
    else:
        #O usuario ja viu todos os filmes da plataforma.
        for match, sim in best_match(users,  person):
            for midx, m in enumerate(movies):
                arr = dataset[[uid for uid, u in enumerate(users) if u == match][0]]
                recommendations.append((m, arr[midx]*sim, person, match))
        return sorted(recommendations, key=lambda x:x[1])

def movies_recommend(recommendations, movies):
    rec = []
    for m in movies:
        m_rec = []
        for m_, w_ , p1, p2 in recommendations:
            if m == m_:
                m_rec.append(w_)
                print((m_, w_ , p1, p2))
        if m_rec:
            rec.append((m, sum(m_rec)/len(m_rec)))
    #return sorted([(m,r) for m, r in rec], key=lambda x:x[1])
    return sorted([(m,100*r/sum([r_ for m_, r_ in rec])) for m, r in rec], key=lambda x:x[1])

def main(): 
    userdata = userDict()
    movies = []
    users = []
    for user in userdata.keys():
        users.append(user)
        for f in userdata[user]:
            movies.append(f)

    movies = np.unique(movies)
    dataset = []
    for idx, u in enumerate(users):
        aux = []
        for f in movies:
            if f in userdata[u]:
                aux.append(int(userdata[u][f]))
            else:
                aux.append(0)
        dataset.append(aux)

    #train = [data for enum, data in enumerate(dataset) if users[enum] != person]
    #predict = dataset[[uid for uid, u in enumerate(users) if u == person][0]]

    person1 = users[5]
    print(best_match(users, person1))
    
    person_recommend = recommend(dataset, users, movies, "123mateus")
    perc_rec = movies_recommend(person_recommend, movies)
    moviearr = []
    for enum, m in enumerate(movies):
        value = [rec_ for m_, rec_ in perc_rec if m_ == m]
        if value != []:
            moviearr.append((m, value[0]))
        else:
            moviearr.append((m, 0.0))

if __name__ == "__main__":
    main()
