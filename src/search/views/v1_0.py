from os import path, getcwd
from flask import Blueprint, json, request
from utils.response import Response
from werkzeug.utils import secure_filename
from ..controllers.userquery import UserQuery
from ..controllers.videovisited import VideoVisited
# from flask import request



basepath = path.basename(__name__).split(".")
root_path = path.join(path.realpath(basepath[0])).split('/{}'.format(basepath[0]))[0]




search = Blueprint('search_v1_0', __name__)

@search.route("/test", methods = ['get', 'post'])
def test():
	try:
		message = {'success': "success"}
		return Response(message, codeStatus=200).Success()
	except Exception as e:
		print("Exception ", e.args)
		return Response(codeStatus=422, hint=str(e)).Error()



@search.route("/solution", methods = ['post'])
def searchSolution():
	try:
		uq = UserQuery(root_path)
		# uq.saveMultimidia()
		uq.saveQuery()
		data = uq.getResult()
		data = {
			"data": data
		}
		return Response(data, codeStatus=200).Success()
	except Exception as e:
		raise e
		print("Exception ", e.args)
		return Response(codeStatus=422, hint=str(e)).Error()


@search.route("/solution/video", methods = ['post'])
def videoWatched():
	try:
		print(dir(request))
		data = {
			"data": "data"
		}
		return Response(data, codeStatus=200).Success()
	except Exception as e:
		# raise e
		print("Exception ", e.args)
		return Response(codeStatus=422, hint=str(e)).Error()