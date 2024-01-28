from rest_framework import serializers

from .models import Channel, Server


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'


class ServerSerializer(serializers.ModelSerializer):
    num_members = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many=True)

    class Meta:
        model = Server
        exclude = ('member',)

    def get_num_members(self, obj):
        if hasattr(obj, 'num_members'):
            return obj.num_members

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data.get("num_members"):
            data.pop('num_members')
        return data
