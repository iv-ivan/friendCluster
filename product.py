import urllib2
import json
import codecs
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pickle
import numpy
from numpy.linalg import solve
from sklearn.neighbors import NearestNeighbors

def loadFriends(myId):
	print "Getting friend list..."
	friendList = json.loads(urllib2.urlopen("https://api.vk.com/method/friends.get?user_id="+str(myId)).read())["response"]
	friendList.append(myId)
	return friendList

def loadWalls(people):
	walls =[]
	print "Getting wall posts"
	for i, pId in enumerate(people):
		answer = json.loads(urllib2.urlopen("https://api.vk.com/method/wall.get?owner_id="+str(pId)+"&offset=0&count=100&owner="+str(pId)).read())
		if answer.has_key("error"):
			continue

		print i*100.0/len(people), "%"
		walls.append([])
		posts = answer["response"][1:]
		for post in posts:
			if (post["post_type"] == "copy"):
				if (post.has_key("copy_text")):
					walls[-1].append(post["copy_text"])
			elif (post.has_key("text")):
				walls[-1].append(post["text"])

	return walls

def save_obj(obj, name ):
    with open('./'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('./' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def printSuperFriends(friends):
	for friend in friends:
		friendList = json.loads(urllib2.urlopen("https://api.vk.com/method/users.get?user_id="+str(friend)).read())["response"][0]
		print friendList["first_name"], friendList["last_name"]


def main():
	myId = 69827345
	friends = loadFriends(myId)#[69827345, 212417383, 86220855]
	wallPosts = loadWalls(uniquePeople)
	walls = []
	for wall in wallPosts:
		walls.append(" ".join(wall))

	vocab = load_obj("vocab")
	Phi = load_obj("Phi")

	vectorizer = CountVectorizer(vocabulary=vocab)
	matr = numpy.transpose(vectorizer.transform(walls))
	features = numpy.transpose(solve(Phi, matr))

	#find nearest to me
	neigh = NearestNeighbors()
	neigh.fit(features)
	mySuperFriends = neigh.kneighbors(features[-1], 10, return_distance=False)
	printSuperFriends(mySuperFriends)

if __name__ == "__main__":
	main()
