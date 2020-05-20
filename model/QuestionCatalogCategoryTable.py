from utils.dbConf import db
from sqlalchemy.sql import func
from datetime import datetime




class QuestionCatalogCategory(db.Model):

	__tablename__ = 'question_catalog_category'

	id = db.Column(db.String(50), primary_key=True)
	category_id = db.Column(db.String(50), db.ForeignKey('question_category.id'), nullable=False, primary_key=True)
	catalog_id = db.Column(db.String(50), db.ForeignKey('question_catalog.id'), nullable=False, primary_key=True)
	is_delete = db.Column(db.Boolean, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
	updated_at = db.Column(db.DateTime, nullable=True, onupdate=func.now())
	deleted_at = db.Column(db.DateTime, nullable=True)
	question_catg = db.relationship('QuestionCategory', backref='question_category')
	question_calg = db.relationship('QuestionCatalog', backref='question_catalog')



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

