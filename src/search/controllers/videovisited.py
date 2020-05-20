from utils.dbConf import WriteSession, ReadSession
from sqlalchemy import desc, or_, and_
from utils.awsService import aws
from datetime import datetime
from threading import Timer
from flask import request
from time import time
from os import getenv
from model import *
import pdfkit
import uuid, math
from flask import Flask , render_template


class VideoVisited:

	def __init__(self, root_path):
		self.root_path = root_path
		self.aws_client = aws()


	def updateVideoStatus(self, req={}):
		"""
		
		"""
		session = ReadSession()
		try:
			if "ref_id" not in req:
				raise Exception("ref_id not found")
			if "video_id" not in req:
				raise Exception("video id not found")

			self.ref_id = req["ref_id"]
			watch_video = session.query(SimilarQuestionPerUser).filter(
				and_(
					SimilarQuestionPerUser.question_id == req["video_id"],
					SimilarQuestionPerUser.query_ref_id == req["ref_id"]
				)
			).all()
			# watch_video = watch_video[0]

			if(not len(watch_video)):
				raise Exception("Video not found")
			elif (watch_video[0].is_last_video):
				# self.runAfter5Min()
				return self.createPDF()
			return 
		except Exception as e:
			session.rollback()
			raise e
		finally:
			session.close()

	def createPDF(self):
		session = WriteSession()
		try:
			all_watched_video = session.query(SimilarQuestionPerUser).filter(
				SimilarQuestionPerUser.query_ref_id == self.ref_id
			).all()
			l = []
			for i in all_watched_video:
				l.append(i.dict_object())

			per_page = 44
			render_string = render_template("questions.html", questions=l, total=len(all_watched_video), total_page = math.ceil(len(all_watched_video)/per_page), per_page=per_page)
			output = 'image_activity/out-{}.pdf'.format("".join(str(time()).split(".")))
			pdf = pdfkit.from_string(render_string, output)
			# print("pdf: ", pdf)

			upload_file_path = self.root_path+"/"+output
			file_name = upload_file_path.split("/")[-1]
			s3_file_path = "{0}/{1}/{2}".format(getenv("IMAGE_PROCESSING_BUCKET"), getenv("SEARCH_IMAGES_BUCKET"), file_name)
			self.file_name = self.aws_client.uploadFileIntoS3(upload_file_path, s3_file_path)

			return self.file_name
		except Exception as e:
			raise e
		finally:
			pass


	def runAfter5Min(self):
		t = Timer(10.0, self.createPDF)
		t.start()



