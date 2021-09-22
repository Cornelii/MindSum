from django.urls import path
from . import views
from .views import MindMapView, NodeView

app_name = 'mind'

urlpatterns = [
    path('', views.minds, name='minds'),
    path('<int:mind_map_id>/', MindMapView.as_view(), name='detail'),
    path('<int:mind_map_id>/<int:node_id>/', NodeView.as_view(), name='node'),
]

