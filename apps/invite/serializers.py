from common.rest_framework.serializers.abstract import PublicIdBaseSerializer


class InviteSerializerSimple(PublicIdBaseSerializer):
    class Meta:
        fields = ('uid',)


class InviteSerializer(PublicIdBaseSerializer):
    class Meta:
        exclude = ('uid',)
