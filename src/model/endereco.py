from	jsonschema	import validate, exceptions
from	mongoengine	import *

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

class Endereco(EmbeddedDocument):
	estado	= StringField(max_length=100, required=True)
	cidade	= StringField(max_length=100, required=True)
	cep		= DecimalField(max_length=9, required=True)
	bairro	= StringField(max_length=100, required=True)
	rua		= StringField(max_length=100, required=True)
	numero	= DecimalField(max_length=4, required=True)
