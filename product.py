import urllib2
import json
import codecs
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pickle
import numpy
from sklearn.neighbors import NearestNeighbors

def loadFriends(myId):
	print "Getting friend list..."
	friendList = json.loads(urllib2.urlopen("https://api.vk.com/method/friends.get?user_id="+str(myId)).read())["response"]
	friendList.append(myId)
	return friendList

def loadWalls(people):
	walls =[]
	accessedFriends = []
	print "Getting wall posts"
	for i, pId in enumerate(people):
		answer = json.loads(urllib2.urlopen("https://api.vk.com/method/wall.get?owner_id="+str(pId)+"&offset=0&count=100&owner="+str(pId)).read())
		if answer.has_key("error"):
			continue

		accessedFriends.append(pId)
		print i*100.0/len(people), "%"
		walls.append([])
		posts = answer["response"][1:]
		for post in posts:
			if (post["post_type"] == "copy"):
				if (post.has_key("copy_text")):
					walls[-1].append(post["copy_text"])
			elif (post.has_key("text")):
				walls[-1].append(post["text"])

	return walls, accessedFriends

def save_obj(obj, name ):
    with open('./'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('./' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def printSuperFriends(friends, accessedFriends):
	for friend in friends:
		friendList = json.loads(urllib2.urlopen("https://api.vk.com/method/users.get?user_ids="+str(accessedFriends[friend])).read())["response"][0]
		print friendList["first_name"], friendList["last_name"]


def main():
	myId = 69827345
	friends = loadFriends(myId)#[69827345, 212417383, 86220855]
	wallPosts, accessedFriends = loadWalls(friends)
	walls = []
	for wall in wallPosts:
		walls.append(" ".join(wall))

	vocab = load_obj("vocab")
	lda = load_obj("Phi")

	vectorizer = CountVectorizer(vocabulary=vocab)

	allFeatures = []
	for i,wall in enumerate(walls):
		userWords = vectorizer.transform([wall])
		features = lda.transform(userWords)[0]
		allFeatures.append(features)

	featuresNumpy = numpy.zeros((len(allFeatures),allFeatures[0].shape[0]))
	for i in xrange(featuresNumpy.shape[0]):
		for j in xrange(featuresNumpy.shape[1]):
			featuresNumpy[i,j] = allFeatures[i][j]

	#find nearest to me
	neigh = NearestNeighbors()
	neigh.fit(featuresNumpy)
	mySuperFriends = neigh.kneighbors(featuresNumpy[-1].reshape(1,-1), 25, return_distance=False)[0]
	printSuperFriends(mySuperFriends, accessedFriends)

if __name__ == "__main__":
	main()
