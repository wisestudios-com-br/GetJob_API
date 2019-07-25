import	hug

from	library.veryx	import auth
from	controller		import curriculo as controllerCurriculo
from	model			import curriculo as modelCurriculo

@hug.get('/', requires=auth.advancedAccess("empresa"))
def get_index(
	response
):
	return controllerCurriculo.getCurriculo(response)

@hug.post('/', requires=auth.ownerAccess())
def post_data(
	curriculo: modelCurriculo.CurriculoType(),
	response
):
	return controllerCurriculo.newCurriculo(response, curriculo)

@hug.put('/', requires=auth.ownerAccess())
def put_data(
	curriculo: modelCurriculo.CurriculoType(),
	response
):
	return controllerCurriculo.updateCurriculo(response, curriculo)

@hug.delete('/', requires=auth.ownerAccess())
def delete_data(
	response
):
	return controllerCurriculo.deleteCurriculo(response)
