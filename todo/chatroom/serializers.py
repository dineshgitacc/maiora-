from rest_framework import serializers
from.models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = ChatMessage
        fields = ('id', 'user', 'message', 'timestamp')