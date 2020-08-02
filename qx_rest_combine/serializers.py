from rest_framework import serializers


query_docs = """
data最大长度10
请求参数:
{
    "request_list": [
        {
            "path": "/api/category/",
            "method": "post",
            "data": {
                "name": "123"
            }
        },
        {
            "path": "/api/category/",
            "method": "get"
        }
    ]
}
"""

response_docs = """
返回结果列表
{
    "response_list": [
        {
            "id": 1,
            "name": "123"
        },
        {}
    ]
}
"""


def validate_for_resource(value):
    if len(value) > 10:
        raise serializers.ValidationError(
            "data max length 10")
    for item in value:
        if not isinstance(item.get('path', ''), str):
            raise serializers.ValidationError(
                "{}, path type error".format(value))
        try:
            method = item.get('method', '').upper()
        except Exception:
            raise serializers.ValidationError(
                "{}, method error".format(value))
        if method not in ['POST', 'PUT', 'PATCH', 'DELETE', 'GET']:
            raise serializers.ValidationError(
                "{}, method error".format(value))


class ResourceSerializer(serializers.Serializer):

    request_list = serializers.ListField(
        label=query_docs, validators=[validate_for_resource])
    response_list = serializers.ListField(
        label=response_docs, read_only=True)
