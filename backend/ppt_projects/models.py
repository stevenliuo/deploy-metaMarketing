from django.db import models

from accounts.models import User


class Project(models.Model):
    """Project model"""

    id = models.BigAutoField(primary_key=True, db_index=True)
    title = models.CharField(max_length=255, verbose_name='Title', default='PPT Project')
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    subtitle = models.CharField(max_length=255, null=True, blank=True, verbose_name='Subtitle')
    footer = models.CharField(max_length=255, null=True, blank=True, verbose_name='Footer')
    template_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Template name')
    is_generating = models.BooleanField(default=False, verbose_name='Is generating?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    template_content = models.BinaryField(null=True, blank=True, verbose_name='Template content')
    ppt_content = models.BinaryField(null=True, blank=True, verbose_name='PPT content')
    screenshot_first_slide = models.FileField(upload_to='slides/screenshot', null=True, blank=True, verbose_name='Screenshot')

    class Meta:
        db_table = 'projects'
        ordering = ['id']

    def __str__(self):
        return self.name


class SlideInstructions(models.Model):
    """Slide instructions model"""

    id = models.BigAutoField(primary_key=True, db_index=True)
    position = models.IntegerField(verbose_name='Position')
    name = models.CharField(max_length=100, verbose_name='Name', default=f'Slide {position}')
    perform_analysis = models.BooleanField(default=False, verbose_name='Perform analysis?')
    display_on_slide = models.BooleanField(default=False, verbose_name='Display on slide?')
    slide_option = models.IntegerField(verbose_name='Slide Option')
    specific_title = models.CharField(max_length=255, null=True, blank=True, verbose_name='Specific title')
    specific_instructions = models.TextField(null=True, blank=True, verbose_name='Specific instructions')
    generated_text = models.TextField(null=True, blank=True, verbose_name='Generated text')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='slide_instructions')
    input_spreadsheet = models.ForeignKey('InputSpreadsheet', on_delete=models.SET_NULL, null=True, blank=True)
    screenshot = models.FileField(upload_to='slides/screenshot', null=True, blank=True, verbose_name='Screenshot')

    class Meta:
        db_table = 'slide_instructions'
        ordering = ['id']

    def __str__(self):
        return self.name


class InputWorkbook(models.Model):
    """Model for collecting .xlsx files"""

    id = models.BigAutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=100, verbose_name='Name')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='input_workbooks')
    content = models.BinaryField(verbose_name='Content')

    class Meta:
        db_table = 'input_workbooks'
        ordering = ['id']

    def __str__(self):
        return self.name


class InputSpreadsheet(models.Model):
    """Model for collecting pages from .xlsx files and for them screenshots"""

    id = models.BigAutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=100, verbose_name='Name')
    position = models.IntegerField(verbose_name='Position')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    input_workbook = models.ForeignKey(InputWorkbook, on_delete=models.CASCADE, related_name='input_spreadsheets')
    screenshot = models.BinaryField(null=True, blank=True, verbose_name='Screenshot')
    content = models.BinaryField(null=True, blank=True, verbose_name='Content')

    class Meta:
        db_table = 'input_spreadsheets'
        ordering = ['id']

    def __str__(self):
        return self.name
