import urllib2
import json

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

def main():
	myId = 69827345
	uniquePeople = loadFriends(myId)

if __name__ == "__main__":
	main()