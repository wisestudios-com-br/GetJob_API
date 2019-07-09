from	model.cliente	import Cliente
from	model.endereco	import Endereco
from	controller		import auth

def newCliente(response, data):
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
