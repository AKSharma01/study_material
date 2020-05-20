from model import QuestionCatalog, QuestionCategory, QuestionCatalogCategory
from utils.dbConf import WriteSession, ReadSession
from sqlalchemy import desc, or_, and_
from random import randrange, choice
from datetime import datetime
from os import getenv
from uuid import uuid4




class CatalogCategoryMapping():
	def __init__(self):
		self.chunk = 100
		pass

	def mapper(self):
		session = ReadSession()
		try:
			self.catalog = session.query(QuestionCatalog).filter(
				and_(
					QuestionCatalog.is_delete == False,
					QuestionCatalog.is_disable==False
				)
			).order_by(QuestionCatalog.id).all()

			self.category = session.query(QuestionCategory).filter(
				and_(
					QuestionCategory.is_delete == False,
					QuestionCategory.is_disable==False
				)
			).order_by(QuestionCategory.id).all()
			self.cata_count = len(self.catalog)
			self.cate_count = len(self.category)
			print("cata_count: ", self.cata_count)
			print("cate_count: ", self.cate_count)
			return self.catalogCategory()
			# return None
		except Exception as e:
			raise e
		finally:
			session.close()


	def catalogCategory(self):
		session = WriteSession()
		result = []
		count = 0
		try:
			for i in range(self.cata_count):
				for j in range(randrange(10)):
					count = count + 1
					val = randrange(self.cate_count)
					temp = QuestionCatalogCategory(
						id = str(uuid4()),
						catalog_id = self.catalog[i].id,
						category_id = self.category[val].id,
						is_delete = False,
						created_at = datetime.now(),
						updated_at = None,
						deleted_at = None
					)
					session.add(temp)
					result.append(temp.dict_object())
					if(count%self.chunk == 0):
						session.commit()
			if(count%self.chunk !=0):
				session.commit()
			return result

		except Exception as e:
			session.rollback()
			raise e
		finally:
			session.close()

		