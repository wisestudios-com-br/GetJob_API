from	pymongo	import MongoClient

db_auth	= MongoClient("mongodb+srv://api:3y3ccSLZtZQlGdoV@getjob-nagfm.mongodb.net").GetJob_Auth
db_data	= MongoClient("mongodb+srv://api:3y3ccSLZtZQlGdoV@getjob-nagfm.mongodb.net").GetJob_Data
