from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LoginUser
from django.contrib.auth.hashers import make_password, check_password
from .serialize import LoginUserSerializer
# Create your views here.



class AppLogin(APIView):
    def post(self,request):
        serializer=LoginUserSerializer(request.data)
        user=LoginUser.objects.filter(user_id=serializer.data['user_id']).first()
        
        if user is None:
            return Response(dict(msg='해당 사용자가 없습니다.'))
        if check_password(serializer.data['user_pw'], user.user_pw):
            return Response(LoginUserSerializer(user).data)
        else:
            return Response(dict(msg='로그인 실패'))

class RegistUser(APIView):
    def post(self,request):
        serializer=LoginUserSerializer(request.data)
        

        user=LoginUser.objects.filter(user_id=serializer.data['user_id']).first()

        if user is not None:
            data=dict(
                msg="이미 존재하는 아이디입니다.",
                user_id=user.user_id,
                user_pw=user.user_pw
            )
            return Response(data)

        
        user = serializer.create(request.data)

        return Response(data=LoginUserSerializer(user).data)

