from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import json

from ppt_projects.models import SlideInstructions, InputWorkbook, Project
from ppt_projects.tasks import create_ppt_task
from ppt_projects.serializers import (
    InputWorkbookSerializer,
    CreateInputWorkbookSerializer,
    CreateSlideInstructionSerializer,
    ProjectSerializer,
    GeneratedProjectSerializer
)


class InputWorkbookListCreateView(generics.ListCreateAPIView):
    """ List .xlsx workbook view """

    queryset = InputWorkbook.objects.all()
    serializer_class = InputWorkbookSerializer

    def get_queryset(self, *args, **kwargs):
        project = Project.objects.get(id=self.kwargs['pk'])
        return super().get_queryset(*args, **kwargs).filter(project=project)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateInputWorkbookSerializer
        return InputWorkbookSerializer


class InputWorkbookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Detail .xlsx workbook view """

    queryset = InputWorkbook.objects.all()
    serializer_class = InputWorkbookSerializer
    lookup_field = 'id'


class SlideInstructionsCreateView(generics.CreateAPIView):
    """ Create slide instruction view """

    queryset = SlideInstructions.objects.all()
    serializer_class = CreateSlideInstructionSerializer


class SlideInstructionsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Detail slide instruction view """

    queryset = SlideInstructions.objects.all()
    serializer_class = CreateSlideInstructionSerializer
    lookup_field = 'id'


class ProjectScreenshotsView(generics.RetrieveAPIView):
    """ Project screenshots view """

    serializer_class = GeneratedProjectSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(user=user)

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': self.request})

        # Check if there is a message in the response
        if 'message' in serializer.data.get('screenshots', {}) or 'error' in serializer.data.get(
                'screenshots', {}):
            return Response(serializer.data['screenshots'], status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectPPTDownloadView(APIView):
    """ Project PPT download view """

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(user=user)

    def get(self, request, pk, format=None):
        try:
            project = Project.objects.get(pk=pk)
            ppt_content = project.ppt_content
            if ppt_content:
                response = HttpResponse(
                    ppt_content,
                    content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation'
                )
                response['Content-Disposition'] = f'attachment; filename="{project.title}.pptx"'
                return response
            else:
                return Response({'error': 'No PPT content available'},
                                status=status.HTTP_404_NOT_FOUND)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


class ProjectListAPIView(generics.ListAPIView):
    """ Project list view """

    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(user=user)


class ProjectCreateAPIView(generics.CreateAPIView):
    """ Project create view """

    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(user=user)


class ProjectUpdateAPIView(generics.RetrieveUpdateAPIView):
    """ Project update view """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDeleteAPIView(generics.DestroyAPIView):
    """ Project delete view """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SlideInstructionDeleteAPIView(generics.DestroyAPIView):
    """
    Endpoint to delete a SlideInstruction instance.
    """
    queryset = SlideInstructions.objects.all()
    serializer_class = SlideInstructionsDetailView

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenerateProjectPPTView(APIView):
    """ Generate project PPT view """

    def post(self, request, pk):
        try:
            project = Project.objects.prefetch_related('slide_instructions').get(id=pk)

            if request.user != project.user:
                return Response({'error': 'You do not have permission to access this project'},
                                status=status.HTTP_403_FORBIDDEN)
            if not project.template_content:
                return Response({'error': 'No template content available'},
                                status=status.HTTP_400_BAD_REQUEST)

            slides = project.slide_instructions.all()

            if not slides:
                return Response({'error': 'Slides are empty'},
                                status=status.HTTP_400_BAD_REQUEST)

            for slide in slides:
                if not slide.input_spreadsheet.screenshot and slide.display_on_slide:
                    return Response(
                        {'message': 'Preparing .xlsx files. This may take some time.'},
                        status=status.HTTP_403_FORBIDDEN
                    )

            create_ppt_task.apply_async(args=(pk, request.user.id))

            return Response({'message': 'PPT generation started'}, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
