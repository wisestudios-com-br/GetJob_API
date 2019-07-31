import	hug
import	numpy
from	jsonschema	import validate, exceptions
from	mongoengine	import *
from	datetime	import datetime

from	.endereco	import schema_endereco, Endereco

schema_empresa	= {
	"type": "object",
	"properties": {
		"nome": {
			"type": "number"
		},
		"senha": {
			"type": "string"
		},
		"atuacao": {
			"type": "string"
		},
		"email": {
			"type": "string"
		},
		"telefone": {
			"type": "string"
		},
		"endereco": schema_endereco,
		"site": {
			"type": "string"
		},
	},
	"required": [
		"cnpj",
		"senha",
		"nome",
		"atuacao",
		"email",
		"telefone",
		"endereco",
		"tipo"
	]
}

class EmpresaType(hug.types.Type):
	__slots__ = ()

	def __call__(self, value):
		try:
			validate(value, schema_empresa)
			return value
		except exceptions.ValidationError as e:
			raise ValueError({
				"invalid":		numpy.array(e.relative_path),
				"required":		e.validator_value
			})

class Empresa(DynamicDocument):
	cnpj			= DecimalField(max_length=14, unique=True, required=True)
	nome			= StringField(max_length=50, required=True)
	senha			= StringField(required=True)
	atuacao			= StringField(max_length=50, required=True)
	email			= StringField(max_length=254, required=True)
	telefone		= StringField(max_length=15, required=True)
	endereco		= EmbeddedDocumentField(Endereco, required=True)
	tipo    		= StringField(max_length=15, required=True)
    site            = StringField(max_length=254)
	timestamp		= DateTimeField(default=datetime.now())
	timeupdate		= DateTimeField(default=datetime.now())
