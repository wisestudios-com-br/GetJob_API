import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.cliente	import Cliente
from	model.endereco	import Endereco
from	controller		import auth

def getClientes(response):
	try:
		data	= json.loads(Cliente.objects.to_json())
		for item in data:
			item.pop('senha')
			item.pop('endereco')
			item.pop('cnh', None) # O campo é opcional, então, caso não exista, retorna None
			item.pop('site', None)
			item.pop('relacionamento', None)
			item.pop('curriculo', None)
		return data

	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def getClienteByCpf(response, cpf):
	try:
		data	= json.loads(Cliente.objects.get(cpf=cpf).to_json())
		data.pop('senha')
		data.pop('curriculo', None)
		return data

	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def newCliente(response, data):
	try:
		endereco		= Endereco(**data["endereco"])
		data["senha"]	= auth.setAuth(response, data["cpf"], data["senha"], "cliente")
		try:
			if data["senha"]["error"]:
				return data["senha"]
		except Exception as e:
			e=e
		data.pop("endereco")
		cliente	= Cliente(endereco=endereco, **data)
		cliente["timestamp"]	= datetime.now()
		cliente["timeupdate"]	= datetime.now()
		cliente.save()
		response.status = HTTP_201
		return json.loads(cliente.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def updateCliente(response, cpf, data):
	locals	= eval(response.get_header("locals"))
	if locals["client_id"] == cpf:
		try:
			endereco	= Endereco(**data["endereco"])
			data.pop("endereco")
			data.pop("senha", None)
			data.pop("_id", None)
			data.pop("timestamp", None)
			data.pop("timeupdate", None)
			cliente					= Cliente.objects.get(cpf=cpf)
			cliente["endereco"]		= endereco
			cliente["timeupdate"]	= datetime.now()
			for key, value in data.items():
				cliente[key]	= value
			cliente.save()
			return json.loads(cliente.to_json())
		except Exception as e:
			response.status = HTTP_502
			return { "error": "bad_gateway" }
	else:
		response.status = HTTP_403
		return { "error" : "access_denied" }

def deleteClienteByCpf(response, cpf):
	locals	= eval(response.get_header("locals"))
	if locals["client_id"] == cpf:
		try:
			delete	= auth.removeAuth(response, cpf)
			if not delete:
				return Cliente.objects.get(cpf=cpf).delete()
			else:
				return delete

		except Exception as e:
			response.status = HTTP_502
			return { "error": "bad_gateway" }
	else:
		response.status = HTTP_403
		return { "error" : "access_denied" }
