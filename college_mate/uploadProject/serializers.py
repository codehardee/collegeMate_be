from rest_framework import serializers
from .models import uploadProject, Bid


class uploadProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = uploadProject
        fields = '__all__'

    def create(self, validated_data):
        # Remove 'student' from validated_data if present
        validated_data.pop('student', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('student', None)  # Prevent student from being modified
        return super().update(instance, validated_data)




# class uploadProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = uploadProject
#         field = '__all__'
#
#         def create(self, validated_data):
#             # Remove 'student' from validated_data if present
#             validated_data.pop('student', None)
#             return super().create(validated_data)
        # fields = ['id', 'title', 'skills', 'scope', 'price', 'description']


class BidSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.student_id')  # Use student_id instead of username

    class Meta:
        model = Bid
        fields = ['id', 'project', 'student', 'bid_amount', 'message', 'created_at']

    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user  # Set the student to the authenticated user
        return super().create(validated_data)

