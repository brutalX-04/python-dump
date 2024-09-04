from flask import Blueprint, send_file, jsonify
from bson import ObjectId
from io import BytesIO
from gridfs import GridFS
from tools.count import update_count
from .delete_file import delete_file
from extensions import mongo
import gridfs

download_bp = Blueprint("download", __name__)


@download_bp.route("/video/<file_id>")
def download_video(file_id):
	try:
		update_count()
		delete_file()
		fs = GridFS(mongo.db, collection="video")
		video = fs.get(ObjectId(file_id))

		if not video:
			return jsonify({ "message": "File not found" }), 404

		return send_file(BytesIO(video.read()), download_name=video.filename, as_attachment=False)

	except gridfs.errors.NoFile:
		return jsonify({ "message": "File not found" }), 404


@download_bp.route("/music/<file_id>")
def download_music(file_id):
	try:
		update_count()
		delete_file()
		fs = GridFS(mongo.db, collection="music")
		music = fs.get(ObjectId(file_id))

		return send_file(BytesIO(music.read()), download_name=music.filename, as_attachment=False)

	except gridfs.errors.NoFile:
		return jsonify({ "message": "File not found" }), 404


@download_bp.route("/image/<file_id>")
def download_image(file_id):
	try:
		update_count()
		delete_file()
		fs = GridFS(mongo.db, collection="image")
		image = fs.get(ObjectId(file_id))

		return send_file(BytesIO(image.read()), download_name=image.filename, as_attachment=False)

	except gridfs.errors.NoFile:
		return jsonify({ "message": "File not found" }), 404