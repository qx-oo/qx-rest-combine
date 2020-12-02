from rest_framework import serializers


def validate_for_resource(value):
    if len(value) > 10:
        raise serializers.ValidationError(
            "data max length 10")
    for item in value:
        if not isinstance(item, dict):
            raise serializers.ValidationError(
                "{}, type error".format(item))
        if not isinstance(item.get('path', ''), str):
            raise serializers.ValidationError(
                "{}, path type error".format(item))
        try:
            method = item.get('method', '').upper()
        except Exception:
            raise serializers.ValidationError(
                "{}, method error".format(item))
        if method not in ['POST', 'PUT', 'PATCH', 'DELETE', 'GET']:
            raise serializers.ValidationError(
                "{}, method error".format(item))
        if data := item.get('data'):
            if not isinstance(data, dict):
                raise serializers.ValidationError(
                    "{}, data error".format(item))


class ResourceSerializer(serializers.Serializer):

    request_list = serializers.ListField(
        label="Request", validators=[validate_for_resource])
    response_list = serializers.ListField(
        label="Response", read_only=True)
