import pymongo
import os
from dotenv import load_dotenv
load_dotenv()


class Storage:
	def __init__(self, user):
		try:
			client = pymongo.MongoClient(os.getenv("MONGO_URI"))
			print("[CONSOLE] Successfully connected to the database")
			mongod = client['myFirstDatabase']
			self.collection = mongod['snake_game']
			# iF the user is an empty string we exit
			self.user = user
			self.userInDb = [i for i in self.collection.find({}, {"name": 1}) if i.get('name') == self.user]

			self.best_score = 0
			if len(self.userInDb) >= 1 and self.userInDb[0]['name'] :
				# print("User already exists")
				self.best_score = [i for i in self.collection.find({"name": user})][0]['best_score']
			else:
				self.collection.insert_one({"name": user, "best_score": 0})
		except:
			print("No hosts found")

	def update(self, score):
		curr_highscore = [score for score in self.collection.find({}, {"_id": 0, "best_score": 1}).sort("best_score", -1).limit(1)][0]
		#Update the overall high score if it's lower than the current score
		if score > curr_highscore['best_score']:
			self.collection.update_one({"best_score": curr_highscore['best_score']}, {"$set":{'best_score': score, "lastSetBy": self.user}})
			if score > self.best_score: #Add the high score to the player's best score
				self.collection.update_one({"name": self.user}, {"$set": {"best_score": score}})
			print(f'Updated by {self.user}')
		else:
			# print("You tried, hopefully you beat your own score")
			if score > self.best_score:
				print(f'You beat your own score {self.best_score} by {score - self.best_score}')
				self.collection.update_one({"name": self.user}, {"$set": {"best_score": score}})

			# print("Can't succeed? Try again.")
	

	def read_highscore(self):
		highscore = [score for score in self.collection.find({}, {"_id": 0, "best_score": 1}).sort("best_score", -1).limit(1)][0]
		set_by = self.collection.find_one({},{"_id": 0, "lastSetBy": 1})['lastSetBy']
		return {'best_score': highscore['best_score'], 'set_by': set_by}
