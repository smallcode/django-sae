from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.http import HttpResponse
import json


class JsonResponse(HttpResponse):
    def __init__(self, obj):
        if isinstance(obj, QuerySet):
            content = serialize('json', obj)
        else:
            content = json.dumps(obj, indent=2, cls=DjangoJSONEncoder, ensure_ascii=False)
        super(JsonResponse, self).__init__(
            content, content_type='application/json')