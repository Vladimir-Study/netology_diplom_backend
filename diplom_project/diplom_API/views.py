from django.contrib.auth.models import User
from django.http import FileResponse
from django.core.exceptions import ValidationError
from rest_framework import mixins, status, parsers
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import UserSerializer, FileDataSerializers, UpdateDataSerializers
from .models import FileData
from datetime import datetime 
import uuid
import pytz
import os


class CheckUser(APIView):

    def post(self, request):
        try:
            get_data = request.data
            user_data = User.objects.get(username=get_data.get('username'))
            check_pwd = user_data.check_password(get_data.get('password'))
            if check_pwd:
                serializers = UserSerializer(user_data)
                content = {'result': serializers.data}
                return Response(content, status=status.HTTP_200_OK)
            else:
                content = {'Error': 'The password does`t match'}
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            content = {'Error': 'User does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class GetFilesAllUsers(APIView):

    permission_classes = [IsAdminUser, IsAuthenticated]

    def get(self, request):
        queryset = FileData.objects.all()
        serializers = FileDataSerializers(queryset, many=True)
        return Response(serializers.data)


class GetFilesUser(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        queryset = FileData.objects.filter(user=id)
        serializers = FileDataSerializers(queryset, many=True)
        return Response(serializers.data)


class UsersCreateView(mixins.CreateModelMixin, 
                        GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

class UsersView(mixins.ListModelMixin,
                mixins.RetrieveModelMixin, 
                mixins.UpdateModelMixin, 
                mixins.DestroyModelMixin,
                GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


# class UsersDestroyView(, 
#                         GenericViewSet):

#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated, IsAdminUser]


class FileDataView(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, 
                   mixins.UpdateModelMixin,
                   GenericViewSet):

    queryset = FileData.objects.all()
    serializer_class = FileDataSerializers
    permission_classes = [IsAuthenticated, ]
    parser_classes = [parsers.MultiPartParser ]

    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user.id)
        user_id = request.GET.get('id')

        if request.user.is_superuser:
            queryset = self.queryset

            if user_id is not None:
                queryset = self.queryset.filter(user=user_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except FileData.DoesNotExist:
            return Response({"Error": f"Запись с id={kwargs.get('pk')} не найдена!"})

        if request.user.id != instance.user_id:
            raise AuthenticationFailed

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.id != instance.user_id:
            raise AuthenticationFailed

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateDataView(mixins.UpdateModelMixin,
                     GenericViewSet):
    
    queryset = FileData.objects.all()
    serializer_class = UpdateDataSerializers
    permission_classes = [IsAuthenticated, IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.id != instance.user_id:
            raise AuthenticationFailed

        return super().update(request, *args, **kwargs)
    

class DownloadFileView(mixins.RetrieveModelMixin,
                       GenericViewSet):
    
    queryset = FileData.objects.all()
    serializer_class = FileDataSerializers
    permission_classes = [IsAuthenticated, ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        tz_moskow = pytz.timezone(os.environ.get('TIMEZONE'))
        instance.last_download_date = datetime.now(tz_moskow)
        instance.save()

        file_handle = instance.filepath.open()
        return FileResponse(file_handle, filename=instance.filepath.name, as_attachment=True)


class GenerateExternalDownloadLinkView(mixins.RetrieveModelMixin,
                       GenericViewSet):
    
    queryset = FileData.objects.all()
    serializer_class = FileDataSerializers
    permission_classes = [IsAuthenticated ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        external_download_uuid = uuid.uuid3(uuid.NAMESPACE_URL, str(instance.filepath))
        instance.external_download_link = external_download_uuid
        instance.save()

        download_link = 'api/v1/download_external_link?uuid='
        link_host = request.build_absolute_uri('/') + download_link
        external_download_link = f'{link_host}{external_download_uuid}'

        return Response({'link': external_download_link})


class ExternalDownloadLinkView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            get_uuid = request.query_params.get('uuid')
            queryset = FileData.objects.get(external_download_link=get_uuid)
        except ValidationError as E:
            return Response({
                'Error': E
            })

        file_handle = queryset.filepath.open()
        return FileResponse(file_handle, filename=queryset.filepath.name, as_attachment=True)