import json
from json import JSONDecodeError

from django.core import serializers
from django.http import HttpResponse


class JsonParser:
    """
    Used for dealing with JSON format
    """
    def get_json_from_req(self, req):
        """
        Converts requests body content to JSON object
        :param req: Http requestget_children object
        :return: JSON object
        """
        try:
            return json.loads(req.body.decode('utf-8'))
        except JSONDecodeError:
            return json.loads('{"error": "Incorrect input"}')

    def get_json_from_obj(self, obj):
        """
        Converts any iterable object to JSON
        :param obj: Any object
        :return: Http response with content type JSON
        """
        try:
            # Try to serialize the object
            data = serializers.serialize('json', obj)
        except AttributeError:
            # Attribute error if the object is a dictionary (already a key value pair)
            data = obj
        return HttpResponse(data, content_type='application/json')