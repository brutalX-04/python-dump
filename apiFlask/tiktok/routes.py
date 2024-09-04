from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from gridfs import GridFS
from tools.count import update_count
from extensions import mongo
import os, re, json, uuid, requests


load_dotenv()
cookies = os.getenv("TIKTOK_COOKIE")

tiktok = Blueprint("tiktok", __name__)


@tiktok.route("/", methods=["GET"])
def home_get():
	update_count()
	response = { "code": 201, "message": "Please send requests POST methode and Json data required" }

	return jsonify(response), 201


@tiktok.route("/", methods=["POST"])
def home_post():
	update_count()
	data = request.get_json()
	output = download(data["url"])

	return jsonify(output)


# -> Download from url
def download(url):
	try:
		with requests.Session() as session:
			headers = {
				'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
				'accept-language': 'en-US,en;q=0.9,id;q=0.8',
				'cache-control': 'max-age=0',
				'priority': 'u=0, i',
				'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
				'sec-ch-ua-mobile': '?0',
				'sec-ch-ua-platform': '"Linux"',
				'sec-fetch-dest': 'document',
				'sec-fetch-mode': 'navigate',
				'sec-fetch-site': 'same-origin',
				'sec-fetch-user': '?1',
				'upgrade-insecure-requests': '1',
				'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
			}

			get  = session.get(url, cookies={"cookie": cookies}, headers=headers)

			# -> Data parsing to json
			details  = re.search('"webapp.video-detail":{(.*?)},"webapp.a-b"', get.text).group(1)
			json_data = json.loads("{"+details+"}")
			items = json_data["itemInfo"]["itemStruct"]

			# -> Path and var
			url_path = "https://brutalx.my.id/download/"
			filename = "download-" + str(uuid.uuid4()).split("-")[0]
			response_json = { "status": "succes", "author": {}, "media": {} }

			# -> Author Information
			data_author = items["author"]
			nickname = data_author["nickname"]
			username = data_author["uniqueId"]
			response_json["author"] = { "username": username, "nickname": nickname }

			# -> Video download handler
			data_video = items["video"]
			url_video = data_video["playAddr"]

			if url_video != "":
				video_name = filename+".mp4"
				video_download = session.get(url_video, cookies={"cookie": cookies}).content
				fs = GridFS(mongo.db, collection="video")

				file_id = fs.put(video_download, filename=video_name)

				response_json["media"]["video"] = "%svideo/%s"%(url_path, file_id)

			else:
				response_json["media"]["video"] = "Failled" 

			# -> Audio download handler
			data_music = items["music"]
			url_music = data_music["playUrl"]

			if url_music != "":
				music_name = filename+".mp3"
				music_download = session.get(url_music, cookies={"cookie": cookies}).content
				fs = GridFS(mongo.db, collection="music")

				file_id = fs.put(music_download, filename=music_name)

				response_json["media"]["music"] = "%smusic/%s"%(url_path, file_id)

			else:
				response_json["media"]["music"] = "Failled"

			return response_json

	except Exception as e:
		return { "status": "Failled", "message": str(e) }
