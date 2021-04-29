from django.conf.urls import url
from django.urls import path

from taskbord.views import Login, Register, CardsListView, Logout, CardCreateView, CardUpdateView, DeleteCardView, \
    MoveCardView

urlpatterns = [
    path('', CardsListView.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('card/create/', CardCreateView.as_view(), name='create-card'),
    path('card/update/<int:pk>/', CardUpdateView.as_view(), name='text-update'),
    path('card/delete/<int:pk>/', DeleteCardView.as_view(), name='delete-card'),
    path('card/move/<int:pk>/', MoveCardView.as_view(), name='move-card'),

]
