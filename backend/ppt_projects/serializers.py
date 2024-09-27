import io
import logging
import tempfile

from rest_framework import serializers
from django.db import transaction
from django.db.models import Max
from pptx import Presentation

from ppt_projects.models import Project, SlideInstructions, InputWorkbook, InputSpreadsheet
from accounts.models import UserSettings
from microservices_tasks.utils import create_screenshot_task
from xlsx_worker import get_workbook_sheet_names

logger = logging.getLogger('ppt_projects.serializer')


class InputSpreadsheetSerializer(serializers.ModelSerializer):
    """ List input spreadsheet serializer """

    class Meta:
        model = InputSpreadsheet
        fields = ['id', 'name', 'position']


class InputWorkbookSerializer(serializers.ModelSerializer):
    """ Workbook serializer """
    content = serializers.FileField(write_only=True)
    name = serializers.CharField(required=False)
    spreadsheets = serializers.SerializerMethodField()

    class Meta:
        model = InputWorkbook
        fields = ['id', 'name', 'spreadsheets', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_spreadsheets(self, obj):
        spreadsheets = InputSpreadsheet.objects.filter(input_workbook=obj)
        return InputSpreadsheetSerializer(spreadsheets, many=True, read_only=True).data

    @staticmethod
    def __check_xlsx_for_the_same_tables(instance, xlsx_content) -> list[InputSpreadsheet]:
        """
        Check xlsx for the same tables
        return: list of InputSpreadsheet items
        raise: serializers.ValidationError if the spreadsheet does not contain the required tables
        """

        old_tables = {(table.position, table.name)
                      for table in InputSpreadsheet.objects.filter(input_workbook=instance)}
        new_tables = {(position, name)
                      for position, name in enumerate(get_workbook_sheet_names(xlsx_content), 1)}

        if not old_tables.issubset(new_tables):
            missing_tables = old_tables - new_tables

            missing_tables_list = [{'name': name, 'position': position}
                                   for position, name in missing_tables]

            missing_tables_list.sort(key=lambda x: int(x['position']))
            raise serializers.ValidationError({
                'error': 'The spreadsheet does not contain the required tables.',
                'content': missing_tables_list
            })

        bulk_items = []

        for table in new_tables - old_tables:
            _table = InputSpreadsheet(name=table[1], position=table[0], input_workbook=instance)

            bulk_items.append(_table)

        return bulk_items

    def update(self, instance, validated_data):

        content = validated_data.pop('content')
        if content.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':

            logging.getLogger('accounts.task').info('Type of loaded file is: %s',
                                                    type(content.file))
            if isinstance(content.file, tempfile._TemporaryFileWrapper):
                with open(content.file.name, 'rb') as f:
                    byte_content = f.read()
            else:
                byte_content = content.file.getvalue()

            tables = self.__check_xlsx_for_the_same_tables(instance, byte_content)

            with transaction.atomic():

                InputSpreadsheet.objects.bulk_create(tables)

                instance.content = byte_content

                instance.name = content.name or instance.name

                instance.save()

            create_screenshot_task(instance)

            instance.spreadsheets = InputSpreadsheet.objects.filter(input_workbook=instance)

            return instance

        else:
            raise serializers.ValidationError("Invalid file type.")


class CreateInputWorkbookSerializer(serializers.ModelSerializer):
    """ Create input workbook serializer """
    content = serializers.FileField(write_only=True)
    name = serializers.CharField(required=False)
    spreadsheets = InputSpreadsheetSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = InputWorkbook
        fields = ['id', 'name', 'content', 'spreadsheets', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    @staticmethod
    def __generate_bulk_input_spreadsheets_items(content, workbook_instance):
        bulk_items = []
        for index, name in enumerate(get_workbook_sheet_names(content), 1):
            item = InputSpreadsheet(name=name, position=index, input_workbook=workbook_instance)
            bulk_items.append(item)

        return bulk_items

    def create(self, validated_data, *args, **kwargs):

        project = Project.objects.get(id=self.context['view'].kwargs['pk'])

        content = validated_data.pop('content')
        # if content.content_type:
        if content.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':

            validated_data['name'] = validated_data.get('name', content.name)

            with transaction.atomic():
                logging.getLogger('accounts.task').info('Type of loaded file is: %s', type(content.file))
                if isinstance(content.file, tempfile._TemporaryFileWrapper):
                    with open(content.file.name, 'rb') as f:
                        byte_content = f.read()
                else:
                    byte_content = content.file.getvalue()

                instance = InputWorkbook.objects.create(
                    project=project, content=byte_content, **validated_data)

                bulk_sheet_items = self.__generate_bulk_input_spreadsheets_items(
                    byte_content, workbook_instance=instance)

                InputSpreadsheet.objects.bulk_create(bulk_sheet_items)

            create_screenshot_task(instance)

            instance.spreadsheets = InputSpreadsheet.objects.filter(input_workbook=instance)

            return instance

        else:
            raise serializers.ValidationError("Invalid file type.")


class CreateSlideInstructionSerializer(serializers.ModelSerializer):
    """ Slide instruction serializer """

    input_spreadsheet = serializers.PrimaryKeyRelatedField(queryset=InputSpreadsheet.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    workbook = serializers.SerializerMethodField()

    class Meta:
        model = SlideInstructions
        fields = ['id', 'position', 'name', 'perform_analysis',
                  'display_on_slide', 'slide_option', 'specific_title',
                  'specific_instructions', 'input_spreadsheet',
                  'workbook', 'project', 'created_at', 'updated_at']

        read_only_fields = ['id', 'position', 'created_at', 'updated_at']

    def validate(self, data):
        # Check if the project is provided in the data
        if 'project' not in data:
            raise serializers.ValidationError("Project is required.")
        return data

    def get_workbook(self, obj):
        return obj.input_spreadsheet.input_workbook.id

    def create(self, validated_data):
        project = validated_data['project']

        project = Project.objects.get(id=project.id)

        if self.context['request'].user != project.user:
            raise serializers.ValidationError(
                "You cannot create slide instructions for this project.")

        # Automatically set the position to the next available position in the project
        max_position = SlideInstructions.objects.filter(project=project).aggregate(
            max_position=Max('position')
        )['max_position']

        next_position = max_position + 1 if max_position is not None else 1
        validated_data['position'] = next_position

        # Set the default name if not provided
        if 'name' not in validated_data or not validated_data['name']:
            validated_data['name'] = f'Slide {next_position}'

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Ensure unique position within the same project on update
        if 'position' in validated_data and validated_data['position'] != instance.position:
            project = validated_data.get('project', instance.project)

            if self.context['request'].user != project.user:
                raise serializers.ValidationError(
                    "You cannot update slide instructions for this project.")

            position = validated_data['position']
            if SlideInstructions.objects.filter(project=project, position=position).exists():
                raise serializers.ValidationError(
                    "This position is already taken within the project.")
        return super().update(instance, validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    """ Project serializer """

    workbook = serializers.SerializerMethodField()
    slides = serializers.SerializerMethodField()
    template_content = serializers.FileField(write_only=True, allow_null=True, required=False)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'subtitle', 'workbook', 'slides',
            'footer', 'template_name', 'template_content', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_workbook(self, obj):
        workbooks = InputWorkbook.objects.all()
        return InputWorkbookSerializer(workbooks, many=True).data

    def get_slides(self, obj):
        slides = SlideInstructions.objects.filter(project=obj)
        return CreateSlideInstructionSerializer(slides, many=True, read_only=True).data

    def create(self, validated_data):
        user = self.context['request'].user
        user_settings = UserSettings.objects.get(user=user)

        project = Project(**validated_data)

        project.user = user

        if not project.template_name:
            project.template_name = user_settings.template_name
        if not project.template_content:
            project.template_content = user_settings.template_content

        project.save()

        return project

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.user != user:
            raise serializers.ValidationError("You cannot update this project.")

        if validated_data.get('template_content'):
            template_content_file = validated_data.pop('template_content')

            if isinstance(template_content_file.file, tempfile._TemporaryFileWrapper):
                with open(template_content_file.file.name, 'rb') as f:
                    byte_content = f.read()
            else:
                byte_content = template_content_file.file.getvalue()

            self.__check_pptx(byte_content)

            instance.template_content = byte_content

        return super().update(instance, validated_data)

    def __check_pptx(self, byte_content: bytes):
        try:
            ppt_content = io.BytesIO(byte_content)
            Presentation(ppt_content)
        except Exception as e:
            logger.error('Invalid file type, error: %s', e, exc_info=True)
            raise serializers.ValidationError("Invalid file type.")


class SlideInstructionScreenshotSerializer(serializers.ModelSerializer):
    """ Slide instruction serializer for generated PPT screenshots """

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    screenshot = serializers.SerializerMethodField()

    class Meta:
        model = SlideInstructions
        fields = ['screenshot', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_screenshot(self, obj):
        request = self.context.get('request')
        if obj.screenshot and hasattr(obj.screenshot, 'url'):
            return request.build_absolute_uri(obj.screenshot.url)
        return None


class GeneratedProjectSerializer(serializers.ModelSerializer):
    """ Generated project serializer with screenshots """

    screenshots = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'screenshot_first_slide', 'screenshots', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_screenshots(self, obj):
        if not obj.ppt_content:

            error_message = {"error": "Generating PPT is not starting yet"}

            if obj.is_generating:
                error_message = {"error": "Generated PPT content empty"}

            return error_message

        slide_instructions = SlideInstructions.objects.filter(project=obj)

        for instruction in slide_instructions:
            if not instruction.screenshot:
                return {"message": "screenshots are not ready"}

        data_list = SlideInstructionScreenshotSerializer(
            slide_instructions, many=True, context=self.context).data

        first_slide_screenshot = {
            'screenshot': self.get_screenshot_first_slide(obj)
        }
        data_list.insert(0, first_slide_screenshot)

        return data_list

    def get_screenshot_first_slide(self, obj):
        request = self.context.get('request')
        if obj.screenshot_first_slide and hasattr(obj.screenshot_first_slide, 'url'):
            return request.build_absolute_uri(obj.screenshot_first_slide.url)
        return None
