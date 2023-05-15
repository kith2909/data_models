import pickle
'''
A simple models performance
'''
model_filename = '/home/kith/Spiced/bergamot-encoder-student-code/weekly_milestones/week_04/data/model_music_best.pkl'
model_filename3 = '/home/kith/Spiced/bergamot-encoder-student-code/weekly_milestones/week_04/data/model_music_best_1.pkl'

model_new = pickle.load(open(model_filename,'rb'))
model_new3 = pickle.load(open(model_filename3,'rb'))

while True:
    str_test = input('Print a test line or print NO to break: ')
    if str_test == "NO":
        break
    print("I know just to groups and I think, this line belongs to group: ", model_new.predict([str_test]))
    print("I know 3 groups and I think, this line belongs to group: ", model_new3.predict([str_test]))
    print('')

