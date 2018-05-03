import pickle

def run(*args):
    data = pickle.load(open('temp.pkl', 'rb'))
    print('Number of Reviews : %d'%(len(data['tag'])))
    print('Number of features : %d'%(len(data['feature'])))
    print(data['feature'])