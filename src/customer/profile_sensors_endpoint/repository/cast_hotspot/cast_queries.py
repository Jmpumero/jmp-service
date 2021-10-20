
from bson.son import SON
from config.config import Settings


from src.customer.repository import MongoQueries
from src.customer.schemas.get import query_params


global_settings = Settings()

cast_connections_proy = {
    '_id':0, 
    'customer_id':1, 
    'data.startDate': 1,
    'data.endDate': 1
}

hotspot_connections_proy = {
    '_id':0, 
    'customer_id':1, 
    'data.date': 1
}

playback_proy = {
    '_id':0,
    'customer_id': 1,
    'data.playback_pair.metadata.title': 1,
    'data.playback_pair.endDate':1,
    'data.playback_pair.startDate':1,    
}

history_proy = {
    '_id': 0,
    'data.startDate': 1,
    'data.playback_pair.appName': 1,
    'data.playback_pair.content': 1,
    'data.playback_pair.startDate': 1,
    'data.playback_pair.endDate': 1,
    'data.deviceId': 1
}

class CastHotSpotQueries(MongoQueries):
    def __init__(self):
        super().__init__()
    
    def count__documents(self, customer_id, sensor):
        if sensor == 'sensor_1':
            count = self.pms_collection.count_documents({'customer_id': customer_id})
        elif sensor == 'sensor_2':
            count = self.cast_collection.count_documents({'customer_id': customer_id})
        elif sensor == 'sensor_3':
            count = self.hotspot_collection.count_documents({'customer_id': customer_id})
        elif sensor == 'sensor_4':
            count = self.butler_collection.count_documents({'customer_id': customer_id})

        return count


    def get_connections(self, customer_id, sensor):
        if sensor == 'sensor_1':
            result = None
        elif sensor == 'sensor_2':
            result = self.cast_collection.find({'customer_id': customer_id}, cast_connections_proy)
        elif sensor == 'sensor_3':
            result = self.hotspot_collection.find({'customer_id': customer_id}, hotspot_connections_proy)
        elif sensor == 'sensor_4':
            result = None

        return result

    def first_connection(self, customer_id, sensor):
        if sensor == 'sensor_1':
            result = None
        elif sensor == 'sensor_2':
            result = self.cast_collection.find({'customer_id': customer_id}, cast_connections_proy
                                               ).sort([('data.startDate', 1)]).limit(1)
        elif sensor == 'sensor_3':
            result = self.hotspot_collection.find({'customer_id': customer_id}, hotspot_connections_proy
                                               ).sort([('data.date', 1)]).limit(1)
        elif sensor == 'sensor_4':
            result = None

        return result

    def last_connection(self, customer_id, sensor):
        if sensor == 'sensor_1':
            result = None
        elif sensor == 'sensor_2':
            result = self.cast_collection.find({'customer_id': customer_id}, cast_connections_proy
                                          ).sort([('data.startDate', -1)]).limit(1)
        elif sensor == 'sensor_3':
            result = self.hotspot_collection.find({'customer_id': customer_id}, hotspot_connections_proy
                                          ).sort([('data.date', -1)]).limit(1)
        elif sensor == 'sensor_4':
            result = None

        return result

    def last_playback(self, customer_id):
        result = self.cast_collection.find({'customer_id': customer_id}, playback_proy).sort([('data.startDate', -1)]).limit(1)
        return result

    def playback_history(self, customer_id, skip, limit):
        if not skip or not limit:
            result = self.cast_collection.find({'customer_id': customer_id}, history_proy)
        else:
            result = self.cast_collection.find({'customer_id': customer_id}, history_proy)
        return result


    def count_connections(self, customer_id):
        pipeline = [
            {
                '$match': { 'customer_id': customer_id } 
            },
            {
                '$group': {
                    '_id': "$data._id",
                    "count": {"$sum": 1}
                }
            }
        ]
        connections = self.cast_collection.aggregate(pipeline)

        return connections

    def group_by_most_used_app(self, customer_id):
        pipeline = [
            {
                '$match': { 'customer_id': customer_id } },
            {
                "$group": {
                    "_id": "$data.playback_pair.appName", 
                    "count": {"$sum": 1}
                    }
            },
            {
                "$sort": SON([("count", -1), ("_id", -1)])
            }
        ]
        most_used = self.cast_collection.aggregate(pipeline)

        return most_used

    def group_by_most_used_device(self, customer_id):
        pipeline = [
            {
                '$match': { 'customer_id': customer_id } },
            {
                "$group": {
                    "_id": "$data.deviceId", 
                    "count": {"$sum": 1}
                    }
            },
            {
                "$sort": SON([("count", -1), ("_id", -1)])
            }
        ]
        most_used = self.cast_collection.aggregate(pipeline)

        return most_used