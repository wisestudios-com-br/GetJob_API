import	json
from	falcon					import HTTP_400, HTTP_403, HTTP_502

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
		print(e)
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
		cliente.save()
		return cliente.to_json()
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }
