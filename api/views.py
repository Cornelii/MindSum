from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mind.models import MindMap, Node
from .serializers import MindMapSerializer, NodeSerializer, TreeSerializer
from rest_framework.views import APIView
from mind.forms import MindMapModelForm, NodeModelForm
from common_lib.common import *
# Create your views here.


class MindMapAPIView(APIView):

    def get(self, *args, **kwargs):
        mind_map_id = kwargs.get('mind_map_id', 0)
        mind_map = MindMap.objects.get(id=mind_map_id)
        root_node = mind_map.root_node
        tree = make_query_set(root_node, 1, mind_map.max_depth)
        print(tree)
        serializer = TreeSerializer(tree, many=True)
        data = recursive_data(make_query_set(root_node, 1, mind_map.max_depth))
        return Response({'response': 'ok', 'nodes': data})

    def post(self, *args, **kwargs):
        form = NodeModelForm(self.request.POST)
        if form.is_valid():
            root_node = form.save(commit=False)
            root_node.depth = 1
            root_node.save()

            form = MindMapModelForm()
            mind_map = form.save(commit=False)
            mind_map.max_depth = 8
            mind_map.root_node = root_node
            mind_map.save()
            return Response({'response': 'ok'})
        else:
            return Response({'response': 'fail'})

    def delete(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass


class NodeAPIView(APIView):

    def get(self, *args, **kwargs):
        node_id = kwargs.get('node_id', 0)
        node = Node.objects.get(id=node_id)
        serializer = NodeSerializer(node)
        return Response(serializer.data)

    def post(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass


@api_view(['GET'])
def subnode(request, node_id):
    root_node = Node.objects.get(id=node_id)
    tree = make_query_set(root_node, 1, 8)
    print(tree)
    serializer = TreeSerializer(tree, many=True)
    data = recursive_data(make_query_set(root_node, 1, 8))
    return Response({'response': 'ok', 'nodes': data})


@api_view(['GET'])
def mind_map_list(request):
    mind_maps = MindMap.objects.all()
    serializer = MindMapSerializer(mind_maps, many=True)
    return Response(serializer.data)

