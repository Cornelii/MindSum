from django.urls import path
from . import views
from .views import MindView, NodeView

app_name = 'api'

urlpatterns = [
    path('', views.mind_map_list, name='mind_map_list'),
    path('mind/<int:mind_map_id>/', MindView.as_view(), name='mind_map'),
    path('node/<int:node_id>/', NodeView.as_view(), name='node'),
    path('node/<int:node_id>/all/', views.subnode, name='subnode'),
]