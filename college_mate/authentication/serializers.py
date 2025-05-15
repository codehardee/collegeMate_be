from rest_framework import serializers
from .models import StudentAccountCreation
# your_app/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['student_id'] = user.student_id  # Add student_id to the token payload
        return token



class StudentAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentAccountCreation
        fields = ['first_name', 'last_name', 'email', 'phone', 'student_id', 'username', 'password']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')

        # Show limited fields for non-admin users
        if not request.user.is_staff:
            # Exclude fields for regular users
            # representation.pop('student_id')
            representation.pop('username')
            representation.pop('password')

        # Remove the password field for everyone (admin included)
        representation.pop('password', None)

        return representation

    def create(self, validated_data):
        user = StudentAccountCreation.objects.create_user(
            student_id=validated_data['student_id'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            username=validated_data.get('username', validated_data['student_id']),
        )
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.username = validated_data.get('username', instance.username)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def validate_password(self, value):
        # Add custom password validation logic here
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value


from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=False)
    student_id = serializers.CharField(max_length=8, required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        if not data.get('username') and not data.get('student_id'):
            raise serializers.ValidationError('Either username or student_id must be provided.')
        return data

# class LoginSerializer(serializers.Serializer):
#     student_id = serializers.CharField(required=True)
#     password = serializers.CharField(required=True)


