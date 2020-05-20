from utils.dbConf import db
from sqlalchemy.sql import func
from datetime import datetime
# from utils.imageObject import ImageClass


class SimilarQuestionPerUser(db.Model):

	__tablename__ = 'similar_question_per_user'

	# id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	id = db.Column(db.String(50), primary_key=True)
	question_id = db.Column(db.String(50), db.ForeignKey('question_catalog.id'), nullable=False)
	question = db.Column(db.String(255), nullable=True)
	query_ref_id = db.Column(db.String(50), nullable=True)
	is_last_video = db.Column(db.Boolean, nullable=False)
	is_disable = db.Column(db.Boolean, nullable=False)
	is_delete = db.Column(db.Boolean, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
	updated_at = db.Column(db.DateTime, nullable=True, onupdate=func.now())
	deleted_at = db.Column(db.DateTime, nullable=True)




	def transformer(self):

		attr_data = self.attr_object()
		dict_data = self.dict_object()
		return {
			"dict_data": dict_data,
			"attr_data": attr_data
		}


	def dict_object(self):
		try:

			columns = list(map(lambda x: (str(x)).split(".")[1], list(self.__table__.columns)))
			dict_data = {}
			for column in columns:
				dict_data[column] = self.__getattribute__(column)
			return dict_data
		except Exception as e:
			print("error: ", e)
			raise e


	def attr_object(self):
		class A:
			def __init__(this):
				pass

		columns = list(map(lambda x: (str(x)).split(".")[1], list(self.__table__.columns)))
		attr_data = A()
		for column in columns:
			setattr(attr_data, str(column), self.__getattribute__(column))
		return attr_data

