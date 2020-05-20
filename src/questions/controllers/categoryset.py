from utils.redisCache import RedisConfig
from utils.dbConf import WriteSession
from random import randrange, choice
from model import QuestionCategory
from datetime import datetime
from uuid import uuid4
from os import getenv
import math




class CategorySet():
	def __init__(self):
		self.redis = RedisConfig()
		self.chunk = 1000

	def generator(self):
		count = self.redis.getValue(getenv("TOTAL_CATEGORY"))
		count = int(count or 0)
		session = WriteSession()
		result = []
		try:
			category_count = randrange(100)
			flag = False
			for i in range(category_count):
				flag = False
				qc = QuestionCategory(
					id = str(uuid4()),
					category = self.categoryName(count+i),
					is_disable = False,
					is_delete = False,
					created_at = datetime.now(),
					updated_at = None,
					deleted_at = None,
				)
				session.add(qc)
				result.append(qc.dict_object())
				if(i % self.chunk == 0):
					session.commit()
					flag = True
			if not flag:
				session.commit()
			count = session.query(QuestionCategory).count()
			self.redis.setValue({getenv("TOTAL_CATEGORY"): count})
			return result
		except Exception as e:
			session.rollback()
			raise e
		finally:
			session.close()



	def categoryName(self, n):
		c = math.floor(n/26)
		r = n%26
		s = []
		for i in range(c):
			s.append(chr(65))

		s.append(chr(65+r))
		s = "".join(s)
		return s
	