import random
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.response import Response
from cms.serializers import UserSerializer
from cms.models import EmailConfirmation

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    @action(methods = ["POST"], detail=False, permission_classes=[permissions.AllowAny])
    def signup(self, request,  *args, **kwargs):
        data = request.data

        #check if the user email exists. If exist direct to login
        if User.objects.filter(email=data["email"]).exists():
            return Response(data={"success" : False, "error" : "User exists."}, status=status.HTTP_409_CONFLICT)
        
        user = User.objects.create(
            username=data["username"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            is_active=False)
        user.set_password(data["password"])
        user.save()
        return Response(data={"success" : True}, status=status.HTTP_200_OK)
    
    @action(methods= ["POST"], detail = False)
    def emailVerification(self, request, *args, **kwargs):
        data = request.data
        code = data["otpcode"]
        confirmation_id = data["confirmation_id"]
        email_confirmation = EmailConfirmation.objects.get(pk = confirmation_id)

        if email_confirmation.code == code :
            user = User.objects.get(email_confirmation.user_id)
            user.is_active = True
            user.save()
            return Response(data={"success" : True}, status=status.HTTP_200_OK)
        else:
            return Response(data={"success" : False, "error" : "Confirmation code not correct"}, status=status.HTTP_400_BAD_REQUEST)
z

    

