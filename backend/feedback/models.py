from django.db import models

from accounts.models import User


class Feedback(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    message = models.TextField()
    url_on_page = models.URLField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
