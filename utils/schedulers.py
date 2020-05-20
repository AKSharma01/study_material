import requests
from .dbConf import ReadSession
from os import getenv, environ
from sqlalchemy import desc
from .redisCache import RedisConfig
from model import QuestionCatalog, QuestionCategory
from apscheduler.scheduler import Scheduler

cron = Scheduler(daemon=True)


cron.start()

redis = RedisConfig()


@cron.interval_schedule(seconds=350)
def cache_latest_catalog_count():
	session	= ReadSession()
	count_key = getenv("TOTAL_CATALOG")
	print("update catalog counts")
	try:
		result = None
		tc = session.query(QuestionCatalog).count()
		
		if(count_key):
			result = redis.getValue(count_key)

		if not result:
			redis.setValue({count_key: tc})
		else:

			result = int(result)
			if(result != tc):
				redis.setValue({count_key: tc})
	except Exception as e:
		session.rollback()
		print("cache_latest_catalog_count: ", e)
	finally:
		session.close()
		pass


@cron.interval_schedule(seconds=300)
def cache_latest_category_count():
	session	= ReadSession()
	count_key = getenv("TOTAL_CATEGORY")
	print("update category counts")
	try:
		result = None
		tc = session.query(QuestionCategory).count()
		
		if(count_key):
			result = redis.getValue(count_key)

		if not result:
			redis.setValue({count_key: tc})
		else:

			result = int(result)
			if(result != tc):
				redis.setValue({count_key: tc})
	except Exception as e:
		session.rollback()
		print("cache_latest_category_count: ", e)
	finally:
		session.close()
		pass
	
