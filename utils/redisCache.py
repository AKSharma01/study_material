import redis
from .config import Setting
from datetime import timedelta

class RedisConfig:

	def __init__(self):
		self.setting = Setting()
		self.setting.createRedisConnectionLink()
		self.connnection = None
		self.connect()

	def connect(self):
		pool = redis.ConnectionPool(
			host=self.setting.host, 
			port=self.setting.port,
			db=self.setting.dbname
		)
		self.connection = redis.Redis(connection_pool=pool)


	def setValue(self, keyValue={}, expire=None):
		try:
			for key in keyValue:
				print("key: {0}, value: {1}".format(key, keyValue[key]))
				self.connection.set(key, keyValue[key], ex=expire)
		except Exception as e:
			# print("error while setting the value: ", e)
			raise e

	def getValue(self, key=None):
		try:
			if key == None:
				raise Exception("key not found")
			else:
				result = self.connection.get(key)
				if result:
					result = result.decode()
				return result
		except Exception as e:
			raise e

	def delKeyValue(self, key=None):
		try:
			if key == None:
				raise Exception("key not found")
			else:
				return self.connection.delete(key)
		except Exception as e:
			raise e




