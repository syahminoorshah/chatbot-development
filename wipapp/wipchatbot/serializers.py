from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = ChatUser
		fields = '__all__'
		extra_kwargs = {'password': {'write_only': True, 'required': True}, 'email': {'required': True}}

	def create(self, validated_data):
		chatuser = ChatUser.objects.create_user(**validated_data)
		Token.objects.create(user=chatuser)
		return chatuser


class ChatLogsSerializer(serializers.ModelSerializer):
	"""docstring for ChatLogsSerializer"""
	class Meta:
		model  = ChatLogs
		fields = '__all__'
