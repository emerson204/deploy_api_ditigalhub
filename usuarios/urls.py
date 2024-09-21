from django.urls import path
from .views import UserRegisterCreateView, UserRegisterListView

urlpatterns = [
  path("registro/list/", UserRegisterListView.as_view()),
  path("registro/create/", UserRegisterCreateView.as_view()),
]
