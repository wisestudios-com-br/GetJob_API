import hug

from	route			import cliente, empresa, vaga
from	library.veryx	import auth

@hug.get('/')
def getIndex():
	return ""

@hug.extend_api('/clientes')
def cliente_api():
	return [cliente]

@hug.extend_api('/empresas')
def empresa_api():
	return [empresa]

@hug.extend_api('/vagas')
def vaga_api():
	return [vaga]
