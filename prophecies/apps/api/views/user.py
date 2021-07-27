from hashlib import md5
from django.contrib.auth.models import User
from rest_framework import viewsets, serializers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

class UserSerializer(serializers.HyperlinkedModelSerializer):
    email_md5 = serializers.SerializerMethodField()

    def get_email_md5(self, user):
        return md5(user.email.encode()).hexdigest()

    class Meta:
        model = User
        fields = ['id', 'url', 'first_name', 'last_name', 'username', 'email', 'email_md5', 'is_staff']


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['email', 'first_name', 'last_name', 'username']
    ordering_fields = ['email', 'first_name', 'last_name', 'username']
    filterset_fields = ['email', 'first_name', 'last_name', 'username', 'is_staff']

    @action(methods=['get'], detail=False)
    def me(self, request, **kwargs):
        """
        Profile of the current user.
        """
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)
