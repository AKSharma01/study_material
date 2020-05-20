from os import getenv, makedirs, path

def create_folders():
	if getenv("IMAGE_ACTIVITY_PATH"):
		image_activity_path = '{}'.format(getenv("IMAGE_ACTIVITY_PATH"))
		if not path.exists(image_activity_path):
			makedirs(image_activity_path)
	if getenv("UPLOAD_FILE_FOLDER"):
		upload_file_folder = '{}'.format(getenv("UPLOAD_FILE_FOLDER"))
		if not path.exists(upload_file_folder):
			makedirs(upload_file_folder)