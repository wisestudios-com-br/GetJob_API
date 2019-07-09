import	hug

from	library.veryx	import auth
from	controller		import cliente as controllerCliente
from	model			import cliente as modelCliente

@hug.get('/', requires=auth.basicAccess())
def get_index():
	return ""

@hug.get('/{id}', requires=auth.basicAccess())
def get_byId(
	id: hug.types.number
):
	return ""

@hug.post('/')
def post_data(
	cliente: modelCliente.ClienteType()
):
	return controllerCliente.newCliente(cliente)

@hug.put('/{id}', requires=auth.basicAccess("cliente"))
def put_data(
	id: hug.types.number,
	cliente: modelCliente.ClienteType()
):
	return ""

@hug.delete('/{id}', requires=auth.basicAccess("cliente"))
def delete_data(
	id: hug.types.number
):
	return ""
