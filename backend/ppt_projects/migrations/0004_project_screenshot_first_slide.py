# Generated by Django 5.0.6 on 2024-06-25 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppt_projects', '0003_project_is_generating'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='screenshot_first_slide',
            field=models.BinaryField(blank=True, null=True, verbose_name='Screenshot first slide'),
        ),
    ]
