from utils.dbConf import WriteSession, ReadSession
from werkzeug.utils import secure_filename
from utils.redisCache import RedisConfig
from sqlalchemy import desc, or_, and_
from utils.awsService import aws
from datetime import datetime
from random import randrange
from flask import request
from time import time
from os import getenv
from model import *
import uuid


class UserQuery:

	def __init__(self, rootPath):
		self.rootPath = rootPath
		self.aws_client = aws()
		self.redis = RedisConfig()
		self.unique_question_set = []
		self.unique_question_ids = []

	def saveMultimidia(self):
		"""
		saveMultimidia function will upload the image in s3 bucket
		"""
		try:
			self.request_headers = {}
			for i in request.headers:
				self.request_headers[i[0]] = i[1]
			# print("request.headers", request.headers)
			
			upload_file_path = '{0}/{1}/file_{2}'.format(self.rootPath, getenv("UPLOAD_FILE_FOLDER"), "".join(str(time()).split(".")))

			if 'files' not in request.files:
				raise Exception("File object not found")

			file = request.files['files']

			if file.filename == '':
				raise Exception("file not available")

			if file:

				filename = secure_filename(file.filename)

				with open(upload_file_path, 'wb') as f:
					f.write(file.stream.read())
					file_name = upload_file_path.split("/")[-1]
					s3_file_path = "{0}/{1}/{2}".format(getenv("IMAGE_PROCESSING_BUCKET"), getenv("SEARCH_IMAGES_BUCKET"), file_name)
					self.file_name = self.aws_client.uploadFileIntoS3(upload_file_path, s3_file_path)
					print("self.file_name: ", self.file_name)
			else:
				raise Exception("file object not found on request")
		except Exception as e:
			raise e


	def saveQuery(self):
		"""
			saveQuery function save the user request detail in user_asked_question table
		"""
		session = WriteSession()
		try:
			self.saveMultimidia()
			# print("self.request_headers: ", self.request_headers)
			uaq = UserAskedQuestion(
				id = str(uuid.uuid4()),
				image_url = self.file_name,
				request_obj = self.request_headers,
				is_response_served = False,
				is_disable = False,
				is_delete = False,
				created_at = datetime.utcnow(),
				updated_at = None,
				deleted_at = None
			)
			session.add(uaq)
			session.commit()
			self.user_question_ref = uaq.id
			return 
		except Exception as e:
			session.rollback()
			raise e
		finally:
			session.close()


	def getResult(self):
		"""
			in getResult function, count is to cache the total count of catalog 
		saved in catalog table 
		n = random no generated within that range (i.e. total catalog count)
		catalog_id is a id to find the category id of that matched catalog
		from QuestionCatalogCategory (which is many-many relation) find out
		the similar question which lay in same category

		"""


		count = self.redis.getValue(getenv("TOTAL_CATALOG"))

		n = randrange(int(count) or 10)

		session = ReadSession()
		try:
			random_data = session.query(QuestionCatalog).filter(
				and_(
					QuestionCatalog.is_delete==False,
					QuestionCatalog.is_disable==False
				)
			).order_by(QuestionCatalog.id).offset(n-1).limit(1).all()

			catalog_id = random_data[0].dict_object()["id"]
			# catalog_id = "9a8b88ab-f408-4377-add8-692c5034ddd6"
			# print("catalog_id: ", catalog_id)
			"""
				for paginating we need to create a track id at 1st 
				and based on that track id can apply the pagination 
				concept for making api smoother
			"""

			
			mapped_val = session.query(QuestionCatalogCategory).filter(
				QuestionCatalogCategory.catalog_id == catalog_id
			).all()

			same_cateogry_question = session.query(
				QuestionCatalogCategory, QuestionCatalog
			).join("question_calg").filter(
				QuestionCatalogCategory.category_id == mapped_val[0].category_id
			).all()
			result = []
			for idx, val in enumerate(same_cateogry_question):
				if idx == len(same_cateogry_question)-1:
					self.last_videos_id = val.QuestionCatalog.id
				solution = val.QuestionCatalog.dict_object()
				category_ids = self.getSuggestedCategories(solution["id"])
				solution["similar_result"] = self.getSuggestedQuestions(category_ids)
				result.append(solution)

			self.saveForRequestedUser()
			return result

		except Exception as e:
			raise e
		finally:
			session.close()


	def getSuggestedCategories(self, question_id=None):
		session = ReadSession()
		try:
			mapped_val = session.query(QuestionCatalogCategory).filter(
				QuestionCatalogCategory.catalog_id == question_id
			).all()
			category_ids = [i.category_id for i in mapped_val]
			return category_ids
		except Exception as e:
			raise e
		finally:
			session.close()
		


	def getSuggestedQuestions(self, category_ids=[]):
		"""
			getSuggestedQuestions function get all the question which belongs to the 
		list of category ids passed in the parameter.
		"""
		session = ReadSession()
		try:
			same_cateogry_question = session.query(
				QuestionCatalogCategory, QuestionCatalog
			).join("question_calg").filter(
				QuestionCatalogCategory.category_id.in_(category_ids)
			).all()
			temp = []
			duplicate_ids = []
			for val in same_cateogry_question:
				val = val.QuestionCatalog.selected_dict_object(["id", "questions"])
				if val["id"] not in duplicate_ids:
					temp.append(val)
					duplicate_ids.append(val["id"])
					self.prepareQuestionSet(val)
			return temp
		except Exception as e:
			raise e
		finally:
			session.close()

	def prepareQuestionSet(self, questionObject=None):
		"""
			prepareQuestionSet prepare the list of unique questions
		"""
		if(questionObject["id"] not in self.unique_question_ids):
			self.unique_question_set.append(questionObject)
			self.unique_question_ids.append(questionObject["id"])

	def saveForRequestedUser(self):
		"""
			found is use to find out the last video solution.
		based on which we return the question set
		"""
		session = WriteSession()
		try:
			found = False
			# print("self.unique_question_set: ", self.unique_question_set)
			print("self.last_videos_id: ", self.last_videos_id)
			for obj in self.unique_question_set:
				if self.last_videos_id == obj["id"]:
					found = True
				sqpu = SimilarQuestionPerUser(
					id = str(uuid.uuid4()),
					question_id = obj["id"],
					question = obj["questions"],
					query_ref_id = self.user_question_ref,
					is_last_video = (self.last_videos_id == obj["id"]),
					is_disable = False,
					is_delete = False,
					created_at = datetime.now(),
					updated_at = None,
					deleted_at = None
				)
				session.add(sqpu)
			if not found:
				session.add(SimilarQuestionPerUser(
					id = str(uuid.uuid4()),
					question_id = obj["id"],
					question = obj["questions"],
					query_ref_id = self.user_question_ref,
					is_last_video = True,
					is_disable = False,
					is_delete = False,
					created_at = datetime.now(),
					updated_at = None,
					deleted_at = None
				))
			
			session.commit()
		except Exception as e:
			session.rollback()
			raise e
		finally:
			session.close()




