from rest_framework import serializers

from feedback.models import Feedback
from feedback.tasks import feedback_task


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ['id', 'message', 'url_on_page', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        instance = Feedback.objects.create(**validated_data)
        feedback_task.apply_async(kwargs={
            "feedback_message": instance.message,
            "feedback_url": instance.url_on_page,
            "user_id": instance.user.id
        })
        return instance
