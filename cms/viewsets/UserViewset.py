import os, random
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.response import Response
from cms.serializers import UserSerializer, ProfileSerializer
from cms.models import EmailConfirmation, Profile
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.db import transaction


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    @transaction.atomic
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
            is_active=True)
        user.set_password(data["password"])
        user.save()
        profile, is_created = Profile.objects.get_or_create(user = user, defaults={"is_verified" : False})
        return Response(data={"success" : True, "user_id" : user.id}, status=status.HTTP_200_OK)
    
    @action(methods= ["POST"], detail = False)
    def emailVerification(self, request, *args, **kwargs):
        # response = {'otpcode': '', 'confirmation_id':  '}
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
        
    # @action(methods=['POST'], detail=False)
    # def googleLogin(self, request):

    @action(methods=['GET'], detail=False)
    def sendEmail(self, request, *args, **kwargs):
        # response = {'email': '', user_id: ''}
        data = request.data
        id = data["user_id"]
        user = User.objects.get(pk= id)
        code = str(round(random.uniform(1, 9) * 100000))

        msg_plain = render_to_string(
           os.path.join(
                     settings.BASE_DIR,
                    "cms",
                    "templates",
                    "email_confirm",
                    "email_confirm.txt"), 
            {"email": data['email'], "code": code}
        )
        send_mail(
            subject='Activate your touracross account',
            message=msg_plain,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[data['email']]
        )
        
        #save the code in the emailConfirmationTable
        confirmation = EmailConfirmation(user=user, code=code)
        confirmation.save()
        return Response(data={'success': True, 'confirmation': confirmation.id}, status=status.HTTP_200_OK)
    
    @action(methods=['GET'], detail=False, permission_classes=[permissions.AllowAny])
    def getData(self, request):
        return Response(data={ 'success' : 'true'}, status=status.HTTP_200_OK)
    
    



    

