from os import path, getcwd
from flask import Blueprint, json, request
from utils.response import Response
from ..controllers.questionset import QuestionSet
from ..controllers.categoryset import CategorySet
from ..controllers.ccmapping import CatalogCategoryMapping
# from flask import request



basepath = path.basename(__name__).split(".")
root_path = path.join(path.realpath(basepath[0])).split('/{}'.format(basepath[0]))[0]




questions_category = Blueprint('questions_category_v1_0', __name__)

@questions_category.route("/test", methods = ['get', 'post'])
def test():
	try:
		message = {'success': "success"}
		return Response(message, codeStatus=200).Success()
	except Exception as e:
		print("ExceptionExceptionExceptionException ", e.args)
		return Response(codeStatus=422, hint=str(e)).Error()



@questions_category.route("/question", methods = ['post'])
def questionsGenerator():
	try:
		qs = QuestionSet()
		result = qs.generator()
		data = {
			"result": result
		}
		return Response(data, codeStatus=200).Success()
	except Exception as e:
		# raise e
		print("ExceptionExceptionExceptionException ", e.args)
		return Response(codeStatus=422, hint=str(e)).Error()

@questions_category.route("/category", methods = ['post'])
def categoryGenerator():
	try:
		cs = CategorySet()
		result = cs.generator()
		data = {
			"result": result
		}
		return Response(data, codeStatus=200).Success()
	except Exception as e:
		# raise e
		print("ExceptionExceptionExceptionException ", e.args)
		return Response(codeStatus=422, hint=str(e)).Error()


@questions_category.route("/mapping", methods = ['post'])
def questionsCategoryGenerator():
	try:
		cs = CatalogCategoryMapping()
		result = cs.mapper()
		data = {
			"result": result
		}
		return Response(data, codeStatus=200).Success()
	except Exception as e:
		# raise e
		print("ExceptionExceptionExceptionException ", e.args)
		return Response(codeStatus=422, hint=str(e)).Error()
