import datetime
from datetime import timedelta

class TimeDiff:

	def __init__(this):
		this.format = '%Y-%m-%d %H:%M:%S.%f'
		this.time = datetime.datetime.now()
		this.formated_date = this.time.strftime(this.format)
		# this.time = this.time.strftime(this.format)


	def diff(this, time):
		try:
			if(type(time.time) is not datetime.datetime):
				raise Exception("time is not datetime type")
			this.__diff = this.time - time.time
			return this.__diff
		except Exception as e:
			raise e
