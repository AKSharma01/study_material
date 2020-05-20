import boto3, sys, threading, datetime, re, random
from os import getenv, makedirs, path, listdir
from werkzeug.utils import secure_filename



class ProgressPercentage:

	def __init__(self, filename):
		self._filename = filename
		self._size = float(os.path.getsize(filename))
		self._seen_so_far = 0
		self._lock = threading.Lock()

	def __call__(self, bytes_amount):
		# To simplify, assume this is hooked up to a single filename
		with self._lock:
			self._seen_so_far += bytes_amount
			percentage = (self._seen_so_far / self._size) * 100
			sys.stdout.write(
				"\r%s  %s / %s  (%.2f%%)" % (
					self._filename, self._seen_so_far, self._size,
					percentage))
			sys.stdout.flush()


class aws:
	"""docstring for aws"""
	def __init__(self):
		try:
			self.s3 = boto3.client('s3',
				region_name=getenv("AWS_REGION_S3"),
				aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
				aws_secret_access_key=getenv("AWS_SECRET_KEY")
			)
		except Exception as e:
			print("error: ", e)
			raise e


	def uploadManager(self, filename, bucketname, objectname):
		self.s3.upload_file(
			filename, bucketname, objectname,
			ExtraArgs={
				'ACL': 'public-read', 
				# 'ContentType': file_detail['mime_type'], 
				'ContentDisposition': 'inline'
			}
			# Callback=ProgressPercentage(filename)
		)
		return '{s3_domain}/{bucketname}/{sub_bucket_filename}'.format(
			s3_domain=getenv("S3_BASE_URL"),
			bucketname=bucketname,
			sub_bucket_filename=objectname
		)

	def uploadFileIntoS3(self, file, sub_bucket_path):
		bucket_path = getenv("AWS_S3_BUCKET")
		uploaded_file = self.uploadManager(file, bucket_path, sub_bucket_path)
		return uploaded_file

##
# To get current month and year
##
def getCurrentMonthAndYear():
	return datetime.date.today().strftime("%B")+datetime.date.today().strftime("%Y")

##
# Get File Name
##
def get_file_name(file):
	file_name = secure_filename(os.path.basename(file.name))
	is_exists = Uploads.objects.filter(name=file_name).count()
	if not is_exists:
		return file_name
	while is_exists:
		random_value = str(random.randint(1,100))
		file_name = file_name.split('.')
		file_name = file_name[0]+random_value+'.'+file_name[1]
		is_exists = Uploads.objects.filter(name=file_name).count()
	return file_name


##
# Get File Extension
##
def get_file_extension(file):
	return os.path.splitext(secure_filename(os.path.basename(file.name)))[1]

##
# Get File Title
##
def get_file_title(file):
	return os.path.splitext(secure_filename(os.path.basename(file.name)))[0]

##
# Get File MIME Type
##
# def get_mime_type(file):
# 	return magic.from_file(UPLOAD_FOLDER+'/'+secure_filename(os.path.basename(file.name)), mime=True)

##
# Get File Path Where File gets uploaded on server
##
def get_file_path(file):
	return UPLOAD_FOLDER+'/'+secure_filename(os.path.basename(file.name))

##
# Get File Size in MB
##
def get_file_size(file):
	return os.path.getsize(get_file_path(file))/1024

##
# Get Allowed Extension
##
def allowed_file(filename):
	ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'doc', 'xls', 'csv']
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
		
