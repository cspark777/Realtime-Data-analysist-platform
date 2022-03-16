from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from streamprocessors.models import StreamProcessor, StreamProcessorStep, WorkflowTask
from streamprocessors.api.serializers import StreamProcessorSerializer, StreamProcessorBaseSerializer, \
    StreamProcessorStepSerializer, SelectChoiceSerializer, WorkflowTaskSerializer
from streamprocessors.utils import choice_to_value_name, STEP_TYPES_DATA, STEP_TYPES


class StreamProcessorViewSet(viewsets.ModelViewSet):
    queryset = StreamProcessor.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('project',)

    def get_serializer_class(self):
        if self.action == 'list':
            return StreamProcessorBaseSerializer
        return StreamProcessorSerializer


class StreamProcessorStepViewSet(viewsets.ModelViewSet):
    queryset = StreamProcessorStep.objects.all()
    serializer_class = StreamProcessorStepSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('streamprocessor',)

    @action(methods=['get'], detail=False, url_path='step-types')
    def get_step_types(self, request, *args, **kwargs):
        step_types = [(a[0],
                       a[1].replace('Processor - ', '')
                       .replace('Data Dictionary Lookup & Replace', 'Dictionary Replace')
                       .replace('Key Performance Indicator', 'KPI')
                       .replace('AWS Comprehend ', ''),
                       a[2]) for a in STEP_TYPES]
        allowed_models = {
            'step_types': step_types,
            'increment_key_types': StreamProcessorStep.INCREMENT_KEY_TYPES,
            'update_key_types': StreamProcessorStep.UPDATE_KEY_TYPES,
        }
        data = {key: choice_to_value_name(value) for key, value in allowed_models.items()}
        data['step_types_data'] = STEP_TYPES_DATA
        serializer = SelectChoiceSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data,  status=status.HTTP_200_OK)


class WorkflowTaskViewSet(viewsets.ModelViewSet):
    queryset = WorkflowTask.objects.all()
    serializer_class = WorkflowTaskSerializer
    permission_classes = (AllowAny,)
