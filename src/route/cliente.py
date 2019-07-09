import hug

@hug.get('/')
def get_index():
	return ""

@hug.get('/{id}')
def get_byId(
	id: hug.types.number
):
	return ""

@hug.post('/')
def post_data(
	cliente: cliente.ClienteType()
):
	return ""

@hug.put('/{id}')
def put_data(
	id: hug.types.number,
	cliente: cliente.ClienteType()
):
	return ""

@hug.delete('/{id}')
def delete_data(
	id: hug.types.number
):
	return ""
