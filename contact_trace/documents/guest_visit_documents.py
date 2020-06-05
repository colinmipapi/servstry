from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from track.models import GuestVisit
from companies.models import Company


@registry.register_document
class GuestVisitIndex(Document):
    class Index:
        name = 'guest_visit'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    name = fields.TextField(
        attr='get_full_name',
        fields={
            'suggest': fields.Completion(),
        }
    )
    company = fields.ObjectField(
        properties={
            'name': fields.TextField(),
            'id': fields.IntegerField(),
        }
    )
    full_name = fields.TextField(attr='get_full_name')

    class Django:
        model = GuestVisit

        fields = (
            'id',
            'first_name',
            'last_name',
            'confirmation'
        )

        related_models = [Company]

    def get_queryset(self):
        return super().get_queryset().select_related(
            'company'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Company):
            return related_instance.guest_visit_set.all()