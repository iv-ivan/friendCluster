import urllib2
import json
import codecs

def loadFriends(myId):
	print "Getting friend list..."
	friendList = json.loads(urllib2.urlopen("https://api.vk.com/method/friends.get?user_id="+str(myId)).read())["response"]
	friendsOfFriends = []
	print "Collecting friends of friend:"
	for friend in friendList:
		print friend
		friendsOfFriends.extend(json.loads(urllib2.urlopen("https://api.vk.com/method/friends.get?user_id="+str(friend)).read())["response"])

	print "Number of non unique FOF: ", len(friendsOfFriends)
	uniquePeople = list(set(friendsOfFriends))
	print "Number of unique FOF: ", len(uniquePeople)
	return uniquePeople

def loadWalls(people):
	walls =[]
	print "Getting wall posts of person:"
	for pId in people:
		walls.append([])
		answer = json.loads(urllib2.urlopen("https://api.vk.com/method/wall.get?owner_id="+str(pId)+"&offset=0&count=100&owner="+str(pId)).read())
		if answer.has_key("error"):
			continue

		print pId
		posts = answer["response"][1:]
		for post in posts:
			if (post["post_type"] == "copy"):
				if (post.has_key("copy_text")):
					walls[-1].append(post["copy_text"])
			elif (post.has_key("text")):
				walls[-1].append(post["text"])

	return walls

def main():
	myId = 69827345
	uniquePeople = loadFriends(myId)#[69827345, 212417383, 86220855]
	wallPosts = loadWalls(uniquePeople)
	with codecs.open("mytxt.txt","w",encoding='utf-8') as f:
		for wall in wallPosts:
			for post in wall:
				f.write(post+"\r\n")

if __name__ == "__main__":
	main()