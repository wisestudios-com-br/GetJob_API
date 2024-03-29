import	hug
import	numpy
from	jsonschema	import validate, exceptions
from	mongoengine	import *
from	datetime	import datetime

from	.curriculo	import schema_curriculo, Curriculo
from	.endereco	import schema_endereco, Endereco

schema_cliente	= {
	"type": "object",
	"properties": {
		"cpf": {
			"type": "number"
		},
		"senha": {
			"type": "string"
		},
		"nome": {
			"type": "string"
		},
		"sobrenome": {
			"type": "string"
		},
		"email": {
			"type": "string"
		},
		"telefone": {
			"type": "string"
		},
		"endereco": schema_endereco,
		"cnh": {
			"type": "string"
		},
		"site": {
			"type": "string"
		},
		"relacionamento": {
			"type": "string"
		},
		"curriculo": schema_curriculo,
	},
	"required": [
		"cpf",
		"senha",
		"nome",
		"sobrenome",
		"email",
		"telefone",
		"endereco"
	]
}

class ClienteType(hug.types.Type):
	__slots__ = ()

	def __call__(self, value):
		try:
			validate(value, schema_cliente)
			return value
		except exceptions.ValidationError as e:
			raise ValueError({
				"invalid":		numpy.array(e.relative_path),
				"required":		e.validator_value
			})

class Cliente(DynamicDocument):
	cpf				= DecimalField(max_length=11, unique=True, required=True)
	nome			= StringField(max_length=50, required=True)
	sobrenome		= StringField(max_length=50, required=True)
	senha			= StringField(required=True)
	email			= StringField(max_length=254, required=True)
	telefone		= StringField(max_length=15, required=True)
	cnh				= BooleanField()
	site			= StringField(max_length=254)
	relacionamento	= BooleanField()
	endereco		= EmbeddedDocumentField(Endereco, required=True)
	curriculo		= EmbeddedDocumentField(Curriculo)
	timestamp		= DateTimeField(default=datetime.now())
	timeupdate		= DateTimeField(default=datetime.now())
