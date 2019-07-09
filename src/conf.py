import	mongoengine

db_auth	= mongoengine.connect(host="mongodb+srv://api:3y3ccSLZtZQlGdoV@getjob-nagfm.mongodb.net/GetJob_Auth", alias="auth").GetJob_Auth
db_data	= mongoengine.connect(host="mongodb+srv://api:3y3ccSLZtZQlGdoV@getjob-nagfm.mongodb.net/GetJob_Data", alias="default").GetJob_Data
