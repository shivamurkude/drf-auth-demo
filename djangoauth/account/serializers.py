from rest_framework.serializers import ModelSerializer ,CharField,ValidationError,EmailField

from .models import User

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