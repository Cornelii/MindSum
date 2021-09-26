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
        return Response({'response': 'ok', 'mind_id': mind_map_id, 'nodes': data})

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
        mind_map_id = kwargs.get('mind_map_id', 0)
        mind_map = get_object_or_404(MindMap, id=mind_map_id)
        root_node = mind_map.root_node
        root_node.delete()
        mind_map.delete()

        return Response({'response': 'ok'})

    def put(self, *args, **kwargs):
        mind_map_id = kwargs.get('mind_map_id', 0)
        mind_map = get_object_or_404(MindMap, id=mind_map_id)
        root_node = mind_map.root_node
        form = NodeModelForm(self.request.POST, instance=root_node)
        if form.is_valid():
            node = form.save(commit=False)
            node.save()

        if kwargs.get('max_depth', 0):
            mind_map.max_depth = int(kwargs.get('max_depth'))
            mind_map.save()

        return Response({'response': 'ok'})



class NodeAPIView(APIView):

    def valid(self, *args, **kwargs):
        mind_map_id = kwargs.get('mind_map_id', 0)
        node_id = kwargs.get('node_id', 0)
        mind_map = get_object_or_404(MindMap, id=mind_map_id)
        node = get_object_or_404(Node, id=node_id)

        return mind_map, node

    def get(self, *args, **kwargs):
        node_id = kwargs.get('node_id', 0)
        node = Node.objects.get(id=node_id)
        serializer = NodeSerializer(node)
        return Response(serializer.data)

    def post(self, *args, **kwargs):
        mind_map, parent_node = self.valid(*args, **kwargs)

        if parent_node.depth >= mind_map.max_depth:
            return Response({'response': 'fail', 'message': 'depth exceeds max value'} )

        form = NodeModelForm(self.requset.POST)
        if form.is_valid():
            new_node = form.save(commit=False)
            new_node.parent = parent_node
            new_node.depth = parent_node.depth + 1
            new_node.save()
            return Response({'response': 'ok'})

        return Response({'response': 'fail', 'message': 'Invalid format'})

    def put(self, *args, **kwargs):
        mind_map, node = self.valid(*args, **kwargs)

        form = NodeModelForm(self.request.POST, instance=node)
        if form.is_valid():
            put_node = form.save()
            return Response({'response': 'ok'})

        return Response({'response': 'fail', 'message': 'Invalid format'})

    def delete(self, *args, **kwargs):
        mind_map, node = self.valid(*args, **kwargs)

        node.delete()

        return Response({'response': 'ok'})


@api_view(['GET'])
def subnode(request, mind_map_id, node_id):
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

