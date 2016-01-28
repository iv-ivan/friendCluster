import urllib2
import json
import codecs
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pickle
import numpy

def save_obj(obj, name ):
    with open('./'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('./' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def main():
	with codecs.open("wallsDB.txt","r",encoding='utf-8') as f:
		walls = f.read().split("\t\n\t")
		vectorizer = CountVectorizer(max_df=0.95, min_df=2)
		F = vectorizer.fit_transform(walls)
		vocab = vectorizer.vocabulary_

		lda = LatentDirichletAllocation(n_topics=1000, max_iter=10,
                                learning_method='online', learning_offset=30.,
                                random_state=777)
		lda.fit(F)
		save_obj(lda, "Phi")
		save_obj(vocab, "vocab")

if __name__ == "__main__":
	main()
