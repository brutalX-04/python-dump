from flask import Blueprint, request, jsonify
from gridfs import GridFS
from tools.count import update_count
from extensions import mongo
import os, re, json, uuid, requests


instagram = Blueprint("instagram", __name__)


@instagram.route("/", methods=["GET"])
def home_get():
	update_count()
	response = { "code": 201, "message": "Please send requests POST methode and Json data required" }

	return jsonify(response), 201


@instagram.route("/", methods=["POST"])
def home_post():
	update_count()
	data = request.get_json()

	url = data.get("url")
	if not url:
		return jsonify({"status": "Error", "message": "url not defined"})

	cookies = data.get("cookies")
	if not cookies:
		return jsonify({"status": "Error", "message": "cookies not defined"})

	output = download(url, cookies)

	return jsonify(output)


# -> Download from url
def download(url, cookies):
	try:
		url_host = "https://brutalx.my.id/download/"
		filename = "download-" + str(uuid.uuid4()).split("-")[0]
		response_json = { "author": {}, "media": {} }

		ids = url.split("/")[4]
		data = requests.get("https://www.instagram.com/p/%s/?__a=1&__d=dis"%(ids), cookies={ "cookie": cookies }).json()
		product_type = data["items"][0]["product_type"]
		response_json["product_type"] = product_type

		author = data["items"][0]["owner"]
		username = author["username"]
		response_json["author"] = { "username": username }


		if product_type == "feed":
			image_name = filename+".jpg"
			image_url = data["items"][0]["image_versions2"]["candidates"][0]["url"]
			image_download = requests.get(image_url).content

			fs = GridFS(mongo.db, collection="image")
			file_id = fs.put(image_download, filename=image_name)

			url_path = url_host+"image/"+str(file_id)
			response_json["media"]["image"] = { "url": url_path }


		elif product_type == "carousel_container":
			carousel_media = data["items"][0]["carousel_media"]
			list_url_image = []
			list_url_video = []
			count=0
			for x in carousel_media:
				image_url = x["image_versions2"]["candidates"][0]["url"]
				try:
					video_url = x["video_versions"][0]["url"]
				except:
					video_url = None

				if video_url:
					filename = filename+str(count)+".mp4"

					fs = GridFS(mongo.db, collection="video")
					file_download = requests.get(video_url).content

					file_id = fs.put(file_download, filename=filename)
					url_path = url_host+"video/"+str(file_id)

					list_url_video.append(url_path)

				else:
					filename = filename+str(count)+".jpg"
					fs = GridFS(mongo.db, collection="image")
					file_download = requests.get(image_url).content

					file_id = fs.put(file_download, filename=filename)
					url_path = url_host+"image/"+str(file_id)

					list_url_image.append(url_path)

				count+=1

			response_json["media"]["image"] = { "url": list_url_image }
			response_json["media"]["video"] = { "url": list_url_video }


		elif product_type == "clips":
			video_name = filename+".mp4"
			video_url = data["items"][0]["video_versions"][0]["url"]
			video_download = requests.get(video_url).content

			fs = GridFS(mongo.db, collection="video")
			file_id = fs.put(video_download, filename=video_name)

			url_path = url_host+"video/"+str(file_id)
			response_json["media"]["video"] = { "url": url_path }

		try:
			music_metadata = data["items"][0]["music_metadata"]

			if music_metadata is None:
				music_url = data["items"][0]["clips_metadata"]["original_sound_info"]["progressive_download_url"]
				if music_url: pass
				else:
					musik_url = None

			else:
				music_url = music_metadata["music_info"]["music_asset_info"]["progressive_download_url"]
				if music_url: pass
				else:
					musik_url = None

			if music_url is not None:
				music_name = filename+".mp3"
				music_download = requests.get(music_url).content

				fs = GridFS(mongo.db, collection="music")
				file_id = fs.put(music_download, filename=music_name)

				url_path = url_host+"music/"+str(file_id)
				response_json["media"]["music"] = { "url": url_path }

			else:
				response_json["media"]["music"] = "None"


		except Exception as e:
			response_json["media"]["music"] = "Failled"


		return response_json

	except Exception as e:
		return { "status": "Failled", "message": str(e) }