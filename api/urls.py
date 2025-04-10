from django.urls import path
from . import views

urlpatterns = [
    path('cat_a_lot_yearfilter', views.year_filter, name='year_filter'),
]