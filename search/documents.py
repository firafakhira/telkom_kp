from django_elasticsearch_dsl import DocType, Index
from hr_wiki.models import Konten

konten = Index('konten')

@konten.doc_type
class KontenDocument(DocType):
    class Meta:
        model = Konten

        fields = [
            'id',
            'judul',
            'isi',
        ]