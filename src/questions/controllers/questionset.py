from model import QuestionCatalog
from random import randrange, choice
from utils.dbConf import WriteSession
from datetime import datetime
from os import getenv
from uuid import uuid4



class QuestionSet():
	def __init__(self):
		self.count = 100
		self.video_domain = getenv("DUMMY_DOMAIN")

	def generator(self):
		session = WriteSession()
		result = []
		try:
			for i in range(self.count):
				temp = QuestionCatalog(
					id = str(uuid4()),
					video_link = "{}{}".format(self.video_domain, self.hashGenerator()),
					questions = self.generateQuestionStatement(),
					is_disable = False,
					is_delete = False,
					created_at = datetime.now(),
					updated_at = None,
					deleted_at = None,
				)
				session.add(temp)
				result.append(temp.dict_object())
			session.commit()
			return result
		except Exception as e:
			session.rollback()
			raise e
		finally:
			session.close()
		
			


	def hashGenerator(self):
		ch = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321+?/"
		
		myval = []
		for i in range(20):
			myval.append(choice(ch))
		myval = ''.join(myval) 
		return myval


	def generateQuestionStatement(self):
		ch = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321"
		statement = []
		state_len = randrange(30) 
		for i in range(10 if state_len <10 else state_len):
			max_word = 8
			n = randrange(max_word)
			for j in range(n):
				if i == 0:
					statement.append(choice(ch).upper())
				else:
					statement.append(choice(ch))
			statement.append(" ")
		statement[len(statement)-1] = "?"
		statement = "".join(statement)
		return statement




		