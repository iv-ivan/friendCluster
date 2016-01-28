import urllib2
import json
import codecs
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def main():
	with codecs.open("wallsDB.txt","r",encoding='utf-8') as f:
		walls = f.read().split("\t\n\t")
		vectorizer = CountVectorizer()#max_df=0.95, min_df=2)
		F = vectorizer.fit_transform(walls)
		vocab = vectorizer.vocabulary_
		stopWords = vectorizer.stop_words_
		lda = LatentDirichletAllocation(n_topics=4, max_iter=7,
                                learning_method='online', learning_offset=30.,
                                random_state=777)
		lda.fit(F)
		Phi = lda.components_
		print Phi

if __name__ == "__main__":
	main()
