import os

class Setting:

	def __init__(self):
		self.env = os.getenv("ENV")
		self.uname = self.password = self.host = self.dbname = ''


	def getDialect(self, dialect):
		if dialect == "MYSQL":
			self.dialect = 'mysql'
		elif dialect == "PSQL":
			self.dialect = 'postgresql'
		elif dialect == "SQLITE":
			self.dialect = 'sqlite'
		else:
			self.dialect = None

	def getSetting(self, dialect='MYSQL', mode="WRITE"):
		self.getDialect(dialect)

		self.uname = os.getenv('{0}_{1}_DB_USER'.format(self.env, dialect))
		self.password = os.getenv('{0}_{1}_DB_PASSWORD'.format(self.env, dialect))
		if mode:
			self.host = os.getenv('{0}_{1}_DB_HOST_{2}'.format(self.env, dialect, mode))
		else:
			self.host = os.getenv('{0}_{1}_DB_HOST'.format(self.env, dialect))
		self.dbname = os.getenv('{0}_{1}_DB_NAME'.format(self.env, dialect))
		self.port = os.getenv('{0}_{1}_DB_PORT'.format(self.env, dialect))



	def createSqlWriteConnetionLink(self, dialect="MYSQL"):
		try:
			self.getSetting(dialect, "WRITE")
			if not self.host:
				raise Exception("undefined write host url")
			return '{dialect}://{uname}:{password}@{host}/{dbname}'.format(
				dialect=self.dialect,
				uname=self.uname,
				password=self.password,
				host=self.host,
				dbname=self.dbname
			)
		except Exception as e:
			print("createSqlWriteConnetionLink: ", e)
		finally:
			self.host = None

	def createSqlReadConnetionLink(self, dialect="MYSQL"):
		try:
			self.getSetting(dialect, "READ")
			if not self.host:
				raise Exception("undefined read host url")
			return '{dialect}://{uname}:{password}@{host}/{dbname}'.format(
				dialect=self.dialect,
				uname=self.uname,
				password=self.password,
				host=self.host,
				dbname=self.dbname
			)
		except Exception as e:
			print("error_createMysqlReadConnetionLink: ", e)
		finally:
			self.host = None

	def createRedisConnectionLink(self):
		self.getSetting('REDIS')