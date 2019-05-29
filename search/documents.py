from django_elasticsearch_dsl import DocType, Index
from hr_wiki.models import Konten, Incident

konten = Index('konten')

@konten.doc_type
class KontenDocument(DocType):
    class Meta:
        model = Konten

        fields = [
            'id',
            'judul',
            'highlight',
            'isi',
        ]

incident = Index('incident')

@incident.doc_type
class IncidentDocument(DocType):
    class Meta:
        model = Incident

        fields = [
            'idincident',
            'kasus',
            'solusi',
        ]