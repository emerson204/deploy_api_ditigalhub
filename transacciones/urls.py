from django.urls import path
from .views import *

urlpatterns = [
  path("ordenes/list/", OrdenesListView.as_view()),
  path("ordenes/create/", OrdenesCreateView.as_view()),
  path("ordenes/update/<int:pk>", OrdenesUpdateView.as_view()),
  path("ordenes/delete/<int:pk>", OrdenesDeleteView.as_view()),
  path("ordenes/pagos/", ProcessPayment.as_view()),
]
