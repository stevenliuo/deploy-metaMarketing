from django.db import models

STATUSES = (
    ('PENDING', 'PENDING'),
    ('COMPLETED', 'COMPLETED'),
    ('FAILED', 'FAILED'),
)


class CreateScreenshotTask(models.Model):
    """Model for creating tasks for screenshots"""

    id = models.BigAutoField(primary_key=True, db_index=True)
    client_uid = models.TextField(default='backend')
    name = models.CharField(max_length=255)
    extra_data = models.TextField(null=True, blank=True)
    content_hash = models.TextField(db_index=True)
    status = models.CharField(choices=STATUSES, default='PENDING')
    status_message = models.TextField(null=True, blank=True)
    content = models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'create_screenshot_tasks'
        ordering = ['id']


class CreateScreenshotTaskScreenshot(models.Model):
    """Model for collecting screenshots from screenshot task"""

    id = models.BigAutoField(primary_key=True, db_index=True)
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    screenshot_task = models.ForeignKey(CreateScreenshotTask, on_delete=models.CASCADE,
                                        related_name='screenshots')
    content = models.BinaryField()

    class Meta:
        db_table = 'create_screenshot_tasks_screenshots'
        ordering = ['id']


class CreatePPTTask(models.Model):
    """Model for creating tasks for creating PPT files"""

    id = models.BigAutoField(primary_key=True, db_index=True)
    client_uid = models.TextField(default='backend')
    name = models.CharField(max_length=255)
    extra_data = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    footer = models.CharField(max_length=255, null=True, blank=True)
    generated_text = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, default='PENDING')
    status_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ppt_template = models.BinaryField(null=True, blank=True)
    created_ppt_content = models.BinaryField(null=True, blank=True)
    screenshot_first_slide = models.BinaryField(null=True, blank=True)

    class Meta:
        db_table = 'create_ppt_tasks'
        ordering = ['id']


class CreatePPTTaskSlide(models.Model):
    """Model for collecting slides from PPT task"""

    id = models.BigAutoField(primary_key=True, db_index=True)
    position = models.IntegerField()
    slide_option = models.IntegerField()
    content = models.TextField()
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ppt_task = models.ForeignKey(CreatePPTTask, on_delete=models.CASCADE,
                                 related_name='ppt_task_slides')
    spreadsheet_screenshot = models.BinaryField(null=True, blank=True)
    screenshot = models.BinaryField(null=True, blank=True)

    class Meta:
        db_table = 'create_ppt_tasks_slides'
        ordering = ['id']


class DuplicatePPTSlidesTask(models.Model):
    """Model for duplicating tasks for microservices"""

    id = models.BigAutoField(primary_key=True, db_index=True)
    client_uid = models.TextField()
    extra_data = models.TextField(null=True, blank=True)
    ppt_in = models.BinaryField()
    ppt_out = models.BinaryField(null=True, blank=True)
    target_count = models.IntegerField()
    status = models.CharField(max_length=255, default='PENDING')
    status_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'duplicate_ppt_slides_tasks'
        ordering = ['id']