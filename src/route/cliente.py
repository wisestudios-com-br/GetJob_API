import	hug

from	library.veryx	import auth
from	controller		import cliente as controllerCliente
from	model			import cliente as modelCliente

@hug.get('/', requires=auth.basicAccess())
def get_index(
	response
):
	return controllerCliente.getClientes(response)

@hug.get('/{id}', requires=auth.basicAccess())
def get_byId(
	id: hug.types.number,
	response
):
	return controllerCliente.getClienteByCpf(response, id)

@hug.post('/')
def post_data(
	cliente: modelCliente.ClienteType(),
	response
):
	return controllerCliente.newCliente(response, cliente)

@hug.put('/{id}', requires=auth.basicAccess("cliente"))
def put_data(
	id: hug.types.number,
	cliente: modelCliente.ClienteType(),
	response
):
	return controllerCliente.updateCliente(response, id, cliente)

@hug.delete('/{id}', requires=auth.basicAccess("cliente"))
def delete_data(
	id: hug.types.number,
	response
):
	return controllerCliente.deleteClienteByCpf(response, id)
