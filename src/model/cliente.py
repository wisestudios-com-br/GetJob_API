import	hug
import	numpy
from	jsonschema	import validate, exceptions
from	mongoengine	import *

from	.curriculo	import schema_curriculo, Curriculo

schema_endereco	= {
	"type":	"object",
	"properties": {
		"estado": {
			"type": "string"
		},
		"cidade": {
			"type": "string"
		},
		"cep": {
			"type": "number"
		},
		"bairro": {
			"type": "string"
		},
		"rua": {
			"type": "string"
		},
		"numero": {
			"type": "number"
		},
	},
	"required": [
		"estado",
		"cidade",
		"cep",
		"bairro",
		"rua",
		"numero"
	]
}

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
			return validate(value, schema_cliente)
		except exceptions.ValidationError as e:
			print(e)
			raise ValueError({
				"invalid":		numpy.array(e.relative_path),
				"required":		e.validator_value
			})

class Endereco(EmbeddedDocument):
	estado	= StringField(max_length=100, required=True)
	cidade	= StringField(max_length=100, required=True)
	cep		= DecimalField(max_length=9, required=True)
	bairro	= StringField(max_length=100, required=True)
	rua		= StringField(max_length=100, required=True)
	numero	= DecimalField(max_length=4, required=True)

class Cliente(DynamicDocument):
	cpf				= DecimalField(max_length=11, required=True)
	nome			= StringField(max_length=50, required=True)
	sobrenome		= StringField(max_length=50, required=True)
	email			= StringField(max_length=254, required=True)
	telefone		= StringField(max_length=15, required=True)
	cnh				= BooleanField()
	site			= StringField(max_length=254)
	relacionamento	= BooleanField()
	endereco		= EmbeddedDocumentField(Endereco, required=True)
	curriculo		= EmbeddedDocumentField(Curriculo)
