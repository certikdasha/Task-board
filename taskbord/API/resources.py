from datetime import datetime, timezone

from django.conf import settings
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from taskbord.API.serializers import CustomUserSerializer, CardSerializer, CardListSerializer
from taskbord.models import CustomUser, Cards, CustomToken


class UserViewSet(CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class LogoutAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class CardCreateAPI(CreateAPIView):

    queryset = Cards.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.initial_data['creator'] = self.request.user.id
        serializer.is_valid(raise_exception=True)
        a = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if not a:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff:
            serializer.save()
        elif 'executor' not in serializer.validated_data:
            serializer.save()
        elif serializer.validated_data['executor'] == user:
            serializer.save()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class DeleteCardAPI(DestroyAPIView):

    queryset = Cards.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAdminUser]


class CardViewSet(viewsets.ModelViewSet):

    queryset = Cards.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['patch'])
    def move_next(self, request, pk=None):
        user = request.user
        card = self.queryset.get(id=pk)
        if card.status < 5 and ((user.is_staff and card.status > 3) or (user == card.executor and card.status < 4)):
            request.data['status'] = card.status + 1
            request.data['creator'] = card.creator.id
            request.data['text'] = card.text
            request.data['executor'] = card.executor.id
            request.data['change_time'] = datetime.now()
            return self.update(request)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['patch'])
    def move_previous(self, request, pk=None):
        user = request.user
        card = self.queryset.get(id=pk)
        if card.status > 1 and ((user.is_staff and card.status == 5) or (user == card.executor and card.status < 5)):
            request.data['status'] = card.status - 1
            request.data['creator'] = card.creator.id
            request.data['text'] = card.text
            request.data['executor'] = card.executor.id
            request.data['change_time'] = datetime.now()
            return self.update(request)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        user = self.request.user
        if user.is_staff:
            if 'creator' in request.data or 'status' in request.data:
                return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                request.data['change_time'] = datetime.now()
                return self.update(request, *args, **kwargs)
        elif user == self.queryset.get(id=kwargs['pk']).creator:
            if len(request.data) == 1 and 'text' in request.data:
                request.data['change_time'] = datetime.now()
                return self.update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['post'])
    def card_list(self, request):
        queryset = Cards.objects.filter(status=request.data['status'])
        serializer = CardListSerializer(queryset, many=True)
        s = serializer.data
        return Response(serializer.data)


class GetCastToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = CustomToken.objects.get_or_create(user=user)
        if token.last_action and (timezone.now() - token.last_action).seconds > settings.AUTO_LOGOUT_DELAY * 60:
            token.delete()
            token, created = CustomToken.objects.get_or_create(user=user)
        return Response({'token': token.key})
