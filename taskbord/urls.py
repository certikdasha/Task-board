from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from taskbord.API.resources import UserViewSet, CardCreateAPI, DeleteCardAPI, CardViewSet
from taskbord.views import Login, Register, CardsListView, Logout, CardCreateView, CardUpdateView, DeleteCardView, \
    MoveCardView

router = routers.SimpleRouter()
router.register(r'card', CardViewSet)


urlpatterns = [
    path('', CardsListView.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('card/create/', CardCreateView.as_view(), name='create-card'),
    path('card/update/<int:pk>/', CardUpdateView.as_view(), name='text-update'),
    path('card/delete/<int:pk>/', DeleteCardView.as_view(), name='delete-card'),
    path('card/move/<int:pk>/', MoveCardView.as_view(), name='move-card'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/register/', UserViewSet.as_view()),
    path('rest/card-create/', CardCreateAPI.as_view()),
    path('rest/delete-card/<int:pk>/', DeleteCardAPI.as_view()),

]
