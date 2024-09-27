from rest_framework import generics

from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer


class CreateFeedbackView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
