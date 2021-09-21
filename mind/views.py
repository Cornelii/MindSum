from django.shortcuts import render, redirect
from .models import Node, MindMap
# Create your views here.


class NodeTree:
    def __init__(self, node):
        self.node = node
        self.children = []


def make_query_set(node, depth=1, max_depth=8):
    if depth > max_depth:
        return
    tree_node = NodeTree(node)
    for child_node in node.children.all():
        tree_node.children.append(make_query_set(child_node, depth+1, max_depth))
    return tree_node


def index(request):

    return render(request, 'mind/index.html')


def minds(request):

    mind_map = MindMap.objects.all()

    return render(request, 'mind/list.html', {'mind_map': mind_map})


def detail(request, mind_map_id):

    mind_map = MindMap.objects.get(id=mind_map_id)
    root_node = mind_map.root_node
    tree = make_query_set(root_node, max_depth=mind_map.max_depth)
    return render(request, 'mind/detail.html', {'tree': tree, 'mind_map_id': mind_map_id})


def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        root_node = Node(title=title, content=content, depth=1)

        root_node.save()

        mind_map = MindMap()
        mind_map.max_depth = 8
        mind_map.root_node = root_node
        mind_map.save()

        return redirect('mind:list')
    else:
        return render(request, 'mind/create.html')



def attach_node(request, mind_map_id, node_id):

    parent_node = Node.objects.get(id=node_id)
    if parent_node.depth >= 8:
        return redirect('mind:detail', mind_map_id)

    new_node = Node()
    new_node.title = request.POST.get("title")
    new_node.content = request.POST.get("content")
    new_node.parent = parent_node
    new_node.depth = parent_node.depth + 1
    new_node.save()

    return redirect('mind:detail', mind_map_id)






