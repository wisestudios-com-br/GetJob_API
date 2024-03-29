import hug

from	route			import auth, cliente, empresa, vaga

@hug.get('/')
def get_index():
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

@hug.extend_api('/oauth')
def auth_api():
	return [auth]
