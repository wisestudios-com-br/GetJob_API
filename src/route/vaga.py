import hug

@hug.get('/')
def getIndex():
	return ""

@hug.get('/{id}')
def getById(
	id: hug.types.number
):
	return ""

@hug.post('/')
def postData():
	return ""

@hug.put('/{id}')
def putData(
	id: hug.types.number
):
	return ""

@hug.delete('/{id}')
def deleteData(
	id: hug.types.number
):
	return ""
