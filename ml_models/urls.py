from django.urls import path
from . import views

urlpatterns = [
    path('predict/<str:symbol>/', views.predict_stock, name='predict_stock'),
    path('model/stats/', views.model_stats, name='model_stats'),
]
