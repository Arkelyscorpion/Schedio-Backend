from django.contrib.auth.models import User
from rest_framework import serializers, validators
from schedio.models import *


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), f"A user with that Email already exists."
                    )
                ],
            },
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user


# class UserProfileSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = UserProfile
#         fields = '__all__'

# class UserPostSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = UserPost
#         fields = '__all__'


class TechStackForPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = TechStackForPost
        fields = '__all__'

class TechStackForUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TechStackForUser
        fields = '__all__'

class ImageUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUrlsForPost
        fields = '__all__'

class TechStackSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TechStackList
        fields = ('tech_name',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email')

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'

# class UserDetailsSerializer(serializers.ModelSerializer): # Serializes all the detials of user and userprofile, nested JSON
#     user = UserSerializer(required=True)
    
#     def create(self,validated_data):
#         user_data = valid


class UserPostSerializer(serializers.ModelSerializer):
    
    
    post_tech_stack = TechStackForPostSerializer(required=False,many=True)
    class Meta:
        model = UserPost
        fields = '__all__'


    
