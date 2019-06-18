from django_elasticsearch_dsl import DocType, Index
from hc_wiki.models import Incident

incident = Index('incident')

@incident.doc_type
class IncidentDocument(DocType):
    class Meta:
        model = Incident

        fields = [
            'idincident',
            'kasus',
            'solusi',
            'applikasi',
            'hits',
        ]