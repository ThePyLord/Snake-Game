import pymongo
import os
from dotenv import load_dotenv
load_dotenv()


class Storage:
	def __init__(self):
		try:
			client = pymongo.MongoClient(os.getenv("MONGO_URI"))
			print("[CONSOLE] Successfully connected to the database")
			mongod = client['myFirstDatabase']
			collection = mongod['snake_game']
			collection.find
		except:
			print("No hosts found")

	def setup(self, username: str):
		self.user = username
		# Look for user in the db

		self.userInDb = [i for i in Storage.collection.find({}, {"name": 1}) if i.get('name') == self.user]
		self.best_score = 0
		if len(self.userInDb) >= 1 and self.userInDb[0]['name'] :
			print("User already exists")
			self.best_score = [i for i in collection.find({"name": self.user})][0]['best_score']
		else:
			Storage.collection.insert_one({"name": self.user, "best_score": 0})


	def update(self, score):
		curr_highscore = [i for i in Storage.collection.find({}, {"_id": 0,"high_score": 1}).limit(1)][0]

		#Update the overall high score if it's lower than the current score
		if score > curr_highscore['high_score']:
			Storage.collection.update_one({"high_score": curr_highscore['high_score']}, {"$set":{'high_score': score, "lastSetBy": self.user}})
			if score > self.best_score: #Add the high score to the player's best score
				Storage.collection.update_one({"name": self.user}, {"$set": {"best_score": score}})
			print(f'Updated by {self.user}')
		else:
			print("You tried, hopefully you beat your own score")
			if score > self.best_score:
				print(f'You beat your own score {self.best_score} by {score - self.best_score}')
				Storage.collection.update_one({"name": self.user}, {"$set": {"best_score": score}})
			else:
				print("Can't succeed? Try again.")
	
	@staticmethod
	def read_highscore():
		highscore = [i for i in Storage.collection.find({}, {"_id": 0, "high_score": 1})][0]
		set_by = Storage.collection.find_one({},{"_id": 0, "lastSetBy": 1})['lastSetBy']

		return {'high_score': highscore['high_score'], 'set_by': set_by}


# C = Database()
# hs_info = Database.read_highscore()
# print(f"The high score: {hs_info['high_score']} was set by: {hs_info['set_by']}")