from django.urls import path
from . import views

app_name = 'mind'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:mind_map_id>/', views.detail, name='detail'),
    path('list/', views.minds, name='list'),
    path('<int:mind_map_id>/<int:node_id>/', views.attach_node, name='attach'),

]

