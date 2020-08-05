from rest_framework import serializers


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
        label="Request", validators=[validate_for_resource])
    response_list = serializers.ListField(
        label="Response", read_only=True)
