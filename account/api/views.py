from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from account.api.serializers import CustomUserSerializer, CustomUserEmailListSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

    @action(methods=['get'], detail=False, url_path='recipient-list')
    def get_email_list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CustomUserEmailListSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
