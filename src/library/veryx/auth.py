import	json
import	jwt
import	os
import	smtplib

from	email.message			import EmailMessage
from	email.headerregistry	import Address
from	email.utils				import make_msgid
from	falcon					import HTTP_400, HTTP_403, HTTP_502
from	datetime				import datetime, timedelta

from	library.cryption	import	cryptKey
from	conf				import	db_auth, db_data

def setAuth(client_id, client_secret, level="cliente"):
	"""Create a new login, with the client_id and the encrypted client_secret"""
	try:
		hash	= cryptKey.newKey()
		secret	= cryptKey.encryptContent(client_secret, hash)
		data	= {
			"client_id"		: client_id,
			"hash"			: hash,
			"level"			: level
		}
		response	= db_auth.auth.insert_one(data)
		if response:
			return secret
		else:
			return False
	except Exception as e:
		return False

def getAuth(client_id, client_secret):
	"""Verify if the login exists"""
	try:
		auths	= db_auth.auth.find_one({ "client_id": client_id })
		datas	= False
		level	= auths['level']
		if level == "cliente":
			datas	= db_data.clientes.find_one({ "cpf": client_id })
		elif level == "empresa":
			datas	= db_data.empresas.find_one({ "cnpj": client_id })
		if response and datas:
			if client_secret == cryptKey.decryptContent(data['senha'], hash['hash']):
				return level
	except Exception as e:
		return False

def getToken(grant_type, client_id, client_secret, response):
	"""Returns a token for an existing client"""
	if grant_type == "client_credentials":
		secret_key	= getSecret()

		level	= getAuth(client_id, client_secret)
		if level:
			return {
				"access_token": jwt.encode({
							"client_id"	: client_id,
							"level"		: level
						}, secret_key, algorithm='HS256'
					).decode('utf8'),
				"token_type": "bearer",
			}
		response.status	= HTTP_400
		return { "error": "invalid_client" }
	response.status	= HTTP_400
	return { "error": "unsupported_grant_type" }

def updateAuth(client_id, client_secret, token, level="cliente"):
	try:
		content	= jwt.decode(token.encode('utf8'), getSecret(), algorithm='HS256')
		expiration = datetime.strptime(content["token_expiration_date"], "%Y-%m-%d %H:%M:%S")
		if client_id == content['client_id']:
			if expiration >= datetime.now():
				return setAuth(client_id, client_secret, level)
	except jwt.DecodeError:
		return False
	return False

def authenticator(function):
	def wrapper(level):
		def authenticate(request, response, **kwargs):
			return function(request, response, level, **kwargs)
		return authenticate
	return wrapper

@authenticator
def basicAccess(request, response, level="basic", context=None, **kwargs):
	"""Token verification"""
	token = request.get_header('Authorization')
	if token:
		if token.split("Bearer ",1)[1]:
			token	= token.split("Bearer ",1)[1]

			secret_key	= getSecret()
			try:
				content	= jwt.decode(token.encode('utf8'), secret_key, algorithm='HS256')
				if content["level"] == level or level == "basic":
					response.append_header('content', content)
					return True
				raise jwt.DecodeError()
			except jwt.DecodeError:
				response.status = HTTP_403
				return { "error" : "access_denied" }
		response.status = HTTP_403
		return { "error" : "access_denied" }
	response.status = HTTP_403
	return { "error" : "access_denied" }

@authenticator
def advancedAccess(request, response, level="empresa", context=None, **kwargs):
	"""Token verification"""
	token = request.get_header('Authorization')
	if token:
		if token.split("Bearer ",1)[1]:
			token	= token.split("Bearer ",1)[1]

			secret_key	= getSecret()

			try:
				user	= jwt.decode(token.encode('utf8'), secret_key, algorithm='HS256')
				id		= request.relative_uri.split('/')[-1]
				if str(user["client_id"]) == str(id) or user["level"] == level:
					return True
			except jwt.DecodeError:
				response.status = HTTP_403
				return { "error" : "access_denied" }
		response.status = HTTP_403
		return { "error" : "access_denied" }
	response.status = HTTP_403
	return { "error" : "access_denied" }

@authenticator
def ownerAccess(request, response, level="basic", context=None, **kwargs):
	"""Token verification"""
	token = request.get_header('Authorization')
	if token:
		if token.split("Bearer ",1)[1]:
			token	= token.split("Bearer ",1)[1]

			secret_key	= getSecret()

			try:
				user	= jwt.decode(token.encode('utf8'), secret_key, algorithm='HS256')
				id		= request.relative_uri.split('/')[-1]
				if str(user['client_id']) == str(id):
					return True
			except jwt.DecodeError:
				response.status = HTTP_403
				return { "error" : "access_denied" }
		response.status = HTTP_403
		return { "error" : "access_denied" }
	response.status = HTTP_403
	return { "error" : "access_denied" }

def sendToken(title, sender, receiver, response):
	token = jwt.encode({
			"client_id": receiver['client_id'],
			"token_expiration_date": format(datetime.now() + timedelta(hours=1), "%Y-%m-%d %H:%M:%S")
		}, getSecret(), algorithm="HS256"
	).decode('utf8')
	link = "https://www.getjob.com.br/reset_password?token=" + token
	msg = EmailMessage()
	msg['Subject'] = title
	msg['From'] = Address(sender['name'], sender['client_id'], sender['email'])
	msg['To'] = (Address(receiver['name'], str(receiver['client_id']), receiver['email']))
	content = """\
	Olá,

	Vimos que esqueceu sua senha, relaxa, com tanta coisa para lembra, é normal.
	Use este link[1] para poder alterar a mesma. Ele irá expirar em breve!

	[1]{0}

	Este é um email automático, não o responda!
	"""
	msg.set_content(content.format(link))

	asparagus_cid = make_msgid()

	content = """\
	<html>
	  <head></head>
	  <body>
		<p>Olá,</p>
		<pVimos que esqueceu sua senha, relaxa, com tanta coisa para lembra, é normal.</br>
		Use este <a href="{0}">link</a> para poder alterar a mesma. Ele irá expirar em breve!</p>
		<p>Este é um email automático, não o responda!</p>
	  </body>
	</html>
	""".format(link, asparagus_cid=asparagus_cid[1:-1])

	msg.add_alternative(content, subtype='html')

	try:
		with smtplib.SMTP('localhost') as s:
			s.send_message(msg)
			return ""
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

	return ""

def getSecret():
	if not os.path.exists('./cache'):
		os.makedirs('./cache')
	if os.path.exists('./cache/secret.json'):
		with open('./cache/secret.json', mode='rb') as privatefile:
			return	json.loads(privatefile.read())['secret']
	else:
		with open('./cache/secret.json', mode='w') as file:
			file.write(json.dumps({ "secret" : cryptKey.newKey() }))
		getSecret()
