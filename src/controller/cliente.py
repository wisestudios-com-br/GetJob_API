from	model.cliente	import Cliente
from	model.endereco	import Endereco

def newCliente(data):
	endereco	= Endereco(**data["endereco"])
	data.pop("endereco")
	cliente	= Cliente(endereco=endereco, **data)
	cliente.save()
	return cliente
