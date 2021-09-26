from django.urls import path
from . import views
from .views import MindMapAPIView, NodeAPIView
from rest_framework_swagger.views import get_swagger_view

app_name = 'api'

api_schema_view = get_swagger_view(title='MindSum API')

urlpatterns = [
    path('', api_schema_view, name='api_doc'),
    path('minds/', views.mind_map_list, name='mind_map_list'),
    path('mind/<int:mind_map_id>/', MindMapAPIView.as_view(), name='mind_map'),
    path('mind/<int:mind_map_id>/<int:node_id>/', NodeAPIView.as_view(), name='node_from_mind'),
    path('mind/<int:mind_map_id>/<int:node_id>/all/', views.subnode, name='subnodes_from_mind'),
    path('node/<int:mind_map_id>/<int:node_id>/', NodeAPIView.as_view(), name='node'),
    path('node/<int:mind_map_id>/<int:node_id>/all/', views.subnode, name='subnodes'),
]