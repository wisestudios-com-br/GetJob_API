import	hug
import	numpy
from	jsonschema	import validate, exceptions
from	mongoengine	import *
from	datetime	import datetime

schema_curriculo	= {
	"type":	"object",
	"properties": {
		"experiencia_emprego": {
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"data_inicio": {
						"type": "string"
					},
					"data_fim": {
						"type": "string"
					},
					"empresa": {
						"type": "string"
					},
					"funcao": {
						"type": "string"
					},
					"observacao": {
						"type": "string"
					},
					"curso": {
						"type": "array",
						"items": {
							"type": "object",
							"properties": {
								"data": {
									"type": "string"
								},
								"titulo": {
									"type": "string"
								},
								"descricao": {
									"type": "string"
								}
							},
							"required": [
								"data",
								"titulo"
							]
						}
					}
				},
				"required": [
					"data_inicio",
					"data_fim",
					"empresa",
					"funcao",
					"observacao"
				]
			}
		},
		"experiencia_outra": {
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"data_inicio": {
						"type": "string"
					},
					"data_fim": {
						"type": "string"
					},
					"tipo": {
						"type": "string"
					},
					"resumo": {
						"type": "string"
					}
				},
				"required": [
					"data_inicio",
					"data_fim",
					"tipo",
					"resumo"
				]
			}
		},
		"escolaridade": {
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"data_inicio": {
						"type": "string"
					},
					"data_fim": {
						"type": "string"
					},
					"grau": {
						"type": "string"
					},
					"local": {
						"type": "string"
					},
					"titulo": {
						"type": "string"
					},
					"anexo": {
						"type": "string"
					}
				},
				"required": [
					"data_inicio",
					"data_fim",
					"grau",
					"local",
					"titulo"
				]
			}
		},
		"referencia": {
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"nome": {
						"type": "string"
					}
				},
				"required": [
					"nome"
				]
			}
		},
		"habilidade": {
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"nome": {
						"type": "string"
					}
				},
				"required": [
					"nome"
				]
			}
		},
		"idioma": {
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"nome": {
						"type": "string"
					}
				},
				"required": [
					"nome"
				]
			}
		},
		"mobilidade": {
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"veiculo": {
						"type": "string"
					}
				},
				"required": [
					"veiculo"
				]
			}
		},
		"remuneracao": {
			"type": "string"
		},
		"objetivo": {
			"type": "string"
		},
		"contato": {
			"type": "object",
			"properties": {
				"email": {
					"type": "string"
				},
				"telefone": {
					"type": "string"
				},
				"social": {
					"type": "array",
					"items": {
						"type": "object",
						"properties": {
							"rede": {
								"type": "string"
							},
							"identificacao": {
								"type": "string"
							}
						},
						"required": [
							"rede",
							"identificacao"
						]
					}
				}
			},
			"required": [
				"email",
				"telefone"
			]
		}
	},
	"required": [
		"remuneracao",
		"objetivo",
		"contato"
	]
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

class Curso(EmbeddedDocument):
	data		= DateField(required=True)
	titulo		= StringField(max_length=100, required=True)
	descricao	= StringField(max_length=500)
	meta		= {'strict': False}

class ExperienciaEmprego(EmbeddedDocument):
	data_inicio	= DateField(required=True)
	data_fim	= DateField(required=True)
	empresa		= StringField(max_length=100, required=True)
	funcao		= StringField(max_length=100, required=True)
	observacao	= StringField(max_length=500, required=True)
	curso		= ListField(EmbeddedDocumentField(Curso))
	meta		= {'strict': False}

class ExperienciaOutra(EmbeddedDocument):
	data_inicio	= DateField(required=True)
	data_fim	= DateField(required=True)
	tipo		= StringField(max_length=50, required=True)
	resumo		= StringField(max_length=1000, required=True)
	meta		= {'strict': False}

class Escolaridade(EmbeddedDocument):
	data_inicio	= DateField(required=True)
	data_fim	= DateField(required=True)
	grau		= StringField(max_length=50, required=True)
	local		= StringField(max_length=100, required=True)
	titulo		= StringField(max_length=100, required=True)
	anexo		= StringField(max_length=500)
	meta		= {'strict': False}

class Nome(EmbeddedDocument):
	nome	= StringField(max_length=100, required=True)
	meta	= {'strict': False}

class Mobilidade(EmbeddedDocument):
	veiculo	= StringField(max_length=100, required=True)

class Social(EmbeddedDocument):
	rede			= StringField(max_length=50, required=True)
	identificacao	= StringField(max_length=50, required=True)
	meta			= {'strict': False}

class Contato(EmbeddedDocument):
	email			= StringField(max_length=254, required=True)
	telefone		= StringField(max_length=15, required=True)
	social			= ListField(EmbeddedDocumentField(Social))
	meta			= {'strict': False}

class Curriculo(EmbeddedDocument):
	experiencia_emprego	= EmbeddedDocumentListField(ExperienciaEmprego)
	experiencia_outra	= EmbeddedDocumentListField(ExperienciaOutra)
	escolaridade		= EmbeddedDocumentListField(Escolaridade)
	referencia			= EmbeddedDocumentListField(Nome)
	habilidade			= EmbeddedDocumentListField(Nome)
	idioma				= EmbeddedDocumentListField(Nome)
	mobilidade			= EmbeddedDocumentListField(Mobilidade)
	remuneracao			= StringField(max_length=10, required=True)
	objetivo			= StringField(max_length=500, required=True)
	contato				= EmbeddedDocumentField(Contato, required=True)
	timestamp			= DateTimeField(default=datetime.utcnow)
	timeupdate			= DateTimeField(default=datetime.utcnow)
	meta				= {'strict': False}
