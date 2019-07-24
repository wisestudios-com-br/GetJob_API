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
						"type": "date"
					},
					"data_fim": {
						"type": "date"
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
									"type": "date"
								},
								"titulo": {
									"type": "string"
								},
								"descricao": {
									"type": "string"
								}
							}
						}
					}
				}
			}
		},
		"experiencia_outra": {
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"data_inicio": {
						"type": "date"
					},
					"data_fim": {
						"type": "date"
					},
					"tipo": {
						"type": "string"
					},
					"resumo": {
						"type": "string"
					},
				}
			}
		},
		"escolaridade": {
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"grau": {
						"type": "string"
					},
					"local": {
						"type": "string"
					},
					"titulo": {
						"type": "string"
					},
					"data_inicio": {
						"type": "date"
					},
					"data_fim": {
						"type": "date"
					},
					"anexo": {
						"type": "string"
					},
				}
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
				}
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
				}
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
				}
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
				}
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
						}
					}
				}

			}
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

class Curso(EmbeddedDocument):
	data		= DateField(required=True)
	titulo		= StringField(max_length=100, required=True)
	descricao	= StringField(max_length=500)

class ExperienciaEmprego(EmbeddedDocument):
	data_inicio	= DateField(required=True)
	data_fim	= DateField(required=True)
	empresa		= StringField(max_length=100, required=True)
	funcao		= StringField(max_length=100, required=True)
	observacao	= StringField(max_length=500, required=True)
	curso		= ListField(EmbeddedDocument(Curso))

class ExperienciaOutra(EmbeddedDocument):
	data_inicio	= DateField(required=True)
	data_fim	= DateField(required=True)
	tipo		= StringField(max_length=50, required=True)
	resumo		= StringField(max_length=1000, required=True)

class Nome(EmbeddedDocument):
	nome	= StringField(max_length=100, required=True)

class Mobilidade(EmbeddedDocument):
	veiculo	= StringField(max_length=100, required=True)

class Social(EmbeddedDocument):
	rede			= StringField(max_length=50, required=True)
	identificacao	= StringField(max_length=50, required=True)

class Contato(EmbeddedDocument):
	email			= StringField(max_length=254, required=True)
	telefone		= StringField(max_length=15, required=True)
	social			= ListField(EmbeddedDocument(Social))

class Curriculo(EmbeddedDocument):
	experiencia_emprego	= ListField(EmbeddedDocumentField(ExperienciaEmprego))
	experiencia_outra	= ListField(EmbeddedDocumentField(ExperienciaOutra))
	escolaridade		= ListField(EmbeddedDocumentField(Escolaridade), required=True)
	referencia			= ListField(EmbeddedDocumentField(Nome))
	habilidade			= ListField(EmbeddedDocumentField(Nome))
	idioma				= ListField(EmbeddedDocumentField(Nome))
	mobilidade			= ListField(EmbeddedDocumentField(Mobilidade))
	remuneracao			= StringField(max_length=10, required=True)
	objetivo			= StringField(max_length=500, required=True)
	contato				= ListField(EmbeddedDocumentField(Contato), required=True)
	timestamp			= DateTimeField(default=datetime.now())
	time_update			= DateTimeField(default=datetime.now())
