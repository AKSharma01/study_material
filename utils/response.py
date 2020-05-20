from flask import json, Response as flask_response, make_response

class Response():

	def __init__(self, data=None, codeStatus='', hint=''):
		self.data = data
		self.codeStatus = codeStatus
		self.hint = hint


	def Success(self):
		try:
			if not self.codeStatus:
				self.codeStatus = 200

			if not self.codeStatus < 400 :
				raise Exception("Status code seems like Failed")

			return make_response({
				"data": (self.data),
				"statue": {
					"status": 'Success',
					"hint": self.hint,
					"statusCode": self.codeStatus
				}
			}, self.codeStatus)
		except Exception as e:
			raise (e)

	def Error(self):
		try:
			if not self.codeStatus:
				self.codeStatus = 400

			if not (self.codeStatus > 400) :
				raise Exception("Status code seems like Success")
			
			return make_response({
				"data": None,
				"state": {
					"status": 'Failed',
					"hint": self.hint,
					"statusCode": self.codeStatus
				}
			}, self.codeStatus)
		except Exception as e:
			raise (e)