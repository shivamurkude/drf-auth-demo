from rest_framework.serializers import ModelSerializer ,CharField,ValidationError,EmailField,Serializer
from django.utils.encoding import smart_bytes,force_bytes,smart_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.core.mail import send_mail
from .models import User
from .utils import Util
class UserRegistrationSerializer(ModelSerializer):
    password2=CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields =("email","name","tc","password","password2")
        extra_kwargs = {
            "password":{
                "write_only":True
            }
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise ValidationError("Passwords and confirm password doesn't match")
        # return attrs
    
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(ModelSerializer):
    email=EmailField(max_length=255)
    class Meta:
        model = User
        fields =["email","password"]
        # extra_kwargs = {
        #     "password":{
        #         "write_only":True
        #     }
        # }
class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields =["id","email","name","tc"]



class UserChangePasswordSerializer(Serializer):
    current_password = CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    new_password = CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    confirm_password = CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ["current_password", "new_password", "confirm_password"]

    def validate(self, attrs):
        current_password = attrs.get('current_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        user = self.context.get('user')

        if not user.check_password(current_password):
            raise ValidationError("Current password is incorrect.")

        if new_password != confirm_password:
            raise ValidationError("New password and confirm password do not match.")

        return attrs

    def save(self):
        user = self.context.get('user')
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
class UserSendPasswordResetEmailSerializer(Serializer):
    email = EmailField(max_length=255)
    class Meta:
        fields = ["email"]
    def validate(self, attrs):
        email = attrs.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError("You do not have an account with us.")
        else:
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print("encoded uid",uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print("password reset token",token)
            link="http://localhost:8000/api/user/reset-password/"+uid+"/"+token+"/"
            print("password reset link",link)

            # send email
            body='Click following link to reset your password '+link
            data={
                "subject":"Reset your password",
                "body":body,
                "to_email":user.email
            }
            Util.send_mail(data)

            # Your email sending code here
            # send_mail(
            #     'Subject',
            #     'Message',
            #     'from@example.com',
            #     ['to@example.com'],
            #     fail_silently=False,
            # )
            return attrs
    
class UserPasswordResetSerializer(Serializer):
    password = CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    class Meta:
        fields = ["password","password2"]
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise ValidationError("Password and confirm password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError("Token is not valid or expired")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError("Token is not valid or expired")