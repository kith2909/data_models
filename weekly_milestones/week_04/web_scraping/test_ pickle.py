import pickle

model_filename = '../data/model_music_best.pkl'

model_new1 = pickle.load(open(model_filename,'rb'))
print(model_new1.predict(['way down','stars sky']))