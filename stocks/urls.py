from django.urls import path
from . import views

urlpatterns = [
    path('<str:symbol>/', views.get_stock_data, name='stock_data'),
    path('<str:symbol>/signal/', views.generate_signal, name='generate_signal'),
    path('signals/recent/', views.get_recent_signals, name='recent_signals'),
    path('search/', views.search_stocks, name='search_stocks'),
    path('market/overview/', views.market_overview, name='market_overview'),
]
