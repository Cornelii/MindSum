from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mind.models import MindMap, Node
from .serializers import MindMapSerializer, NodeSerializer, TreeSerializer
from django.views import View
from rest_framework.views import APIView
# Create your views here.

class NodeTree:
    def __init__(self, node):
        self.node = node
        self.children = []

def make_query_set(node, depth = 1, max_depth = 8):
    if depth > max_depth:
        return
    tree_node = NodeTree(node)
    for child_node in node.children.all():
        tree_node.children.append(make_query_set(child_node, depth+1, max_depth))
    return tree_node

def recursive_data(instance):
    a = {'title':instance.node.title, 'content':instance.node.content, 'depth':instance.node.depth}
    children = []
    for node in instance.children:
        children.append(recursive_data(node))
    a['children'] = children
    return a


class MindView(APIView):

    def get(self, *args, **kwargs):
        mind_map_id = kwargs.get('mind_map_id', 0)
        mind_map = MindMap.objects.get(id=mind_map_id)
        root_node = mind_map.root_node
        tree = make_query_set(root_node, 1, mind_map.max_depth)
        print(tree)
        serializer = TreeSerializer(tree, many=True)
        data = recursive_data(make_query_set(root_node, 1, mind_map.max_depth))
        return Response({'reponse': 'ok', 'nodes': data})

    def post(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

class NodeView(APIView):

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
    return Response({'reponse': 'ok', 'nodes': data})


@api_view(['GET'])
def mind_map_list(request):
    mind_maps = MindMap.objects.all()
    serializer = MindMapSerializer(mind_maps, many=True)
    return Response(serializer.data)