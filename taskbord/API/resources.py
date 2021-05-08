from datetime import datetime

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from taskbord.API.serializers import CustomUserSerializer, CardSerializer, CardListSerializer
from taskbord.models import CustomUser, Cards


class UserViewSet(CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class LoginAPIView(APIView):
    pass
#


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
