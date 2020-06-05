from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from companies.models import Company


@registry.register_document
class CompanyIndex(Document):
    class Index:
        name = 'company'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    name = fields.TextField(
        attr='name',
        fields={
            'suggest': fields.Completion(),
        }
    )
    get_absolute_url = fields.TextField(attr="get_absolute_url")

    class Django:
        model = Company