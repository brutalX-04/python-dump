from gridfs import GridFS
from extensions import mongo
import pytz


collection_list = ["image", "video", "music"]

def delete_file():
	for collection_name in collection_list:
		from datetime import datetime, timedelta
		threshold_time = datetime.now(pytz.utc) - timedelta(minutes=3)

		fs = GridFS(mongo.db, collection=collection_name)
		file_data = fs.find({ "uploadDate": { "$lt": threshold_time } })

		for file in file_data:
			fs.delete(file._id)
