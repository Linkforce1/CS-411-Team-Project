from math import exp, log
from . import train
import operator

type_dic = {0:"workout", 1:"party", 2:"dinner", 3:"sleep", 4:"party"}
# def initiate(list, proj_dic, songs, rel_dic):
#     for i in len(list):
#         if i + 1 < len(list):
#             proj_dic[list[i].name, list[i + 1].name] = \
#             res.get((list[i].name, list[i + 1].name), 0) + 1
#             songs[list[i].name] = songs.get(list[i].name, 0) + 1

def transform(playlist, popularity, type = -1):
    artists = []
    songs = playlist.keys()
    for song in songs:
        artists = artists + playlist[song][1]
        if type != -1:
            # print(type)
            # print(len(pop[2]))
            popularity[type][song] = playlist[song][0]
    return artists


class classifier(object):
    def fit(self, train_set, train_label):
        self.v = set()
        self.prior = [0] * 5
        self.dic = {l:dict() for l in train_label}
        for i in range(len(train_set)):
            self.prior[train_label[i]] += 1
            for w in train_set[i]:
                self.v.add(w)
                self.dic[train_label[i]][w] = \
                self.dic[train_label[i]].get(w, 0) + 1
        self.num_words = len(self.v)


    def predict(self, list):
        accuracy = 0.0
        res = []
        smoother = 0.01
        smoother_bi = 2.5
        uni_res = []
        for i in range(5):
            uni_res.append(sum(log((self.dic[i].get(w, 0) + smoother) \
            /(sum(self.dic[i].values()) + self.num_words * smoother)) \
            for w in list))
        return uni_res.index(max(uni_res))


# The code below are the main function,
#
# make train.test a dictionary in train.py,
# type_dic[res] will be the type of it and the top_ten_song
# are recommended songs based on the type of the test playlist
def do_recommendation(song_dict):
    arts = []
    types = []
    pop = {l:dict() for l in range(5)}
    for i in train.workout:
        a = transform(i, pop, 0)
        arts.append(a)
        types.append(0)
    for i in train.party:
        a = transform(i, pop, 1)
        arts.append(a)
        types.append(1)
    for i in train.dinner:
        a = transform(i, pop, 2)
        arts.append(a)
        types.append(2)
    for i in train.sleep:
        a = transform(i, pop, 3)
        arts.append(a)
        types.append(3)
    for i in train.focus:
        a = transform(i, pop, 4)
        arts.append(a)
        types.append(4)
    c = classifier()
    c.fit(arts, types)
    res1 = []
    res2 = []
    for i in song_dict:
        temp = c.predict(transform(i, None))
        res1.append(temp)

    for j in range(len(song_dict)):
        sorted1 = sorted(pop[res1[j]].items(), key = operator.itemgetter(1))
        top_ten_songs = []
        for i in range(10):
            top_ten_songs.append(sorted1[::-1][i][0])
        res2.append(top_ten_songs)
    # print([k for j in range(5) for k in train.focus[j] if k in train.test])
    # print([k for j in range(5) for k in train.sleep[j] if k in train.test])
    return res1, res2

if __name__ == "__main__":
    print(do_recommendation())
