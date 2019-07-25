import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.cliente	import Cliente
from	model.curriculo	import *
from	controller		import auth

def getCurriculo(response):
	locals	= eval(response.get_header("locals"))
	try:
		curriculo	= Cliente.objects.get(cpf=locals["id"]).curriculo
		data		= []
		if curriculo:
			data	= json.loads(curriculo.to_json())
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def newCurriculo(response, data):
	locals	= eval(response.get_header("locals"))
	try:
		cliente	= Cliente.objects.get(cpf=locals["client_id"])
		if cliente["curriculo"] is None:
			curriculo			= Curriculo(**data)
			cliente.update(**{
				"set__curriculo": data
			})
			cliente.save()
			response.status = HTTP_201
			return json.loads(curriculo.to_json())
		else:
			response.status = HTTP_403
			return json.loads(cliente["curriculo"].to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def updateCurriculo(response, data):
	locals	= eval(response.get_header("locals"))
	try:
		cliente	= Cliente.objects.get(cpf=locals["client_id"])
		data.pop("timestamp", None)
		data["timeupdate"]	= datetime.now()
		curriculo			= Curriculo(**data)
		cliente.update(**{
			"set__curriculo": data
		})
		cliente.save()
		return json.loads(curriculo.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def deleteCurriculo(response):
	locals	= eval(response.get_header("locals"))
	try:
		cliente	= Cliente.objects.get(cpf=locals["client_id"])
		cliente.update(unset__curriculo=1)
		cliente.save()
		return {}
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }
