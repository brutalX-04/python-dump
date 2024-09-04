from extensions import mongo

def get_count():
    data_count = mongo.db.request_count.find_one({})
    count = data_count.get("count") if data_count else 0

    return str(count)


def update_count():
    data_count = mongo.db.request_count.find_one({})
    count = data_count.get("count") if data_count else 0

    mongo.db.request_count.update_one({}, {"$set": { "count": int(count)+1 }}, upsert=True)