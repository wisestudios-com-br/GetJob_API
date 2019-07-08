import	hug
import	numpy
from	jsonschema	import validate, exceptions
from	model		import cliente

@hug.get('/')
def getIndex():
	return ""

@hug.get('/{id}')
def getById(
	id: hug.types.number
):
	return ""

@hug.post('/')
def postData(
	cliente: cliente.ClienteType()
):
	return ""

@hug.put('/{id}')
def putData(
	id: hug.types.number,
	cliente: cliente.ClienteType()
):
	return ""

@hug.delete('/{id}')
def deleteData(
	id: hug.types.number
):
	return ""
