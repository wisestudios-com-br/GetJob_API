import	hug
import	numpy
from	jsonschema	import validate, exceptions
from	mongoengine	import *
from	datetime	import datetime

schema_curriculo	= {
	"type":	"object",
	"properties": {
		"experiencias": {
			"type": "array"
		},
		"escolaridade": {
			"type": "array"
		},
		"referencias": {
			"type": "array"
		},
		"habilidades": {
			"type": "array"
		},
		"idiomas": {
			"type": "array"
		},
		"mobilidade": {
			"type": "string"
		},
		"remuneracao": {
			"type": "string"
		},
		"objetivo": {
			"type": "string"
		},
		"contato": {
			"type": "array"
		}
	}
}

class CurriculoType(hug.types.Type):
	__slots__ = ()

	def __call__(self, value):
		try:
			validate(value, schema_curriculo)
			return value
		except exceptions.ValidationError as e:
			raise ValueError({
				"atribute":	numpy.array(e.relative_path),
				"type":		e.validator_value
			})

class Curriculo(EmbeddedDocument):
	experiencias	= ListField(GenericEmbeddedDocumentField())
	escolaridade	= ListField(GenericEmbeddedDocumentField())
	referencias		= ListField(GenericEmbeddedDocumentField())
	habilidades		= ListField(GenericEmbeddedDocumentField())
	idiomas			= ListField(GenericEmbeddedDocumentField())
	mobilidade		= StringField(max_length=100, required=True)
	remuneracao		= StringField(max_length=10, required=True)
	objetivo		= StringField(max_length=500, required=True)
	contato			= ListField(GenericEmbeddedDocumentField())
	timestamp		= DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	time_update		= DateTimeField(efault=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
