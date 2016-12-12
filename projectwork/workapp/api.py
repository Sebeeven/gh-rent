from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from workapp.models import UserInfo

class UserInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserInfo
		fields = '__all__'

@api_view(['GET'])
def userlist(request):
	user_list = UserInfo.objects.all()
	serializer = UserInfoSerializer(user_list, many=True)
	return Response(serializer.data)
