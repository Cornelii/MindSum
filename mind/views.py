from django.shortcuts import render, redirect, get_object_or_404
from .models import Node, MindMap
from django.views import View
from .forms import NodeModelForm, MindMapModelForm
from common_lib.common import *
# Create your views here.


class MindMapView(View):

    def dispatch(self, request, *args, **kwargs):
        method = request.POST.get('_method')
        if isinstance(method, str):
            method = method.lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        elif method == 'delete':
            return self.delete(*args, **kwargs)
        else:
            return super(MindMapView, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        mind_map_id = kwargs.get('mind_map_id', 0)
        mind_map = get_object_or_404(MindMap, id=mind_map_id)
        root_node = mind_map.root_node
        tree = make_query_set(root_node, max_depth=mind_map.max_depth)
        return render(self.request, 'mind/detail.html', {'tree': tree, 'mind_map_id': mind_map_id})

    def post(self, *args, **kwargs):
        forms = NodeModelForm(self.request.POST)
        if forms.is_valid():
            root_node = forms.save(commit=False)
            root_node.depth = 1
            root_node.save()

            forms = MindMapModelForm()
            mind_map = forms.save(commit=False)
            mind_map.max_depth = 8
            mind_map.root_node = root_node
            mind_map.save()

        return redirect('mind:minds')

    def put(self, *args, **kwargs):

        form = NodeModelForm(self.request.POST)

    def delete(self, *args, **kwargs):
        pass


def minds(request):

    mind_map = MindMap.objects.all()
    form = NodeModelForm

    return render(request, 'mind/list.html', {'mind_map': mind_map, 'form': form})


class NodeView(View):

    def valid(self, *args, **kwargs):
        mind_map_id = kwargs.get('mind_map_id', 0)
        node_id = kwargs.get('node_id', 0)

        mind_map = get_object_or_404(MindMap, id=mind_map_id)
        node = get_object_or_404(Node, id=node_id)

        return mind_map, node

    def dispatch(self, request, *args, **kwargs):
        method = request.POST.get('_method')

        if method == 'put':
            return self.put(*args, **kwargs)
        elif method == 'delete':
            return self.delete(*args, **kwargs)
        else:
            return super(NodeView, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        mind_map, parent_node = self.valid(*args, **kwargs)
        if parent_node.depth >= mind_map.max_depth:
            return redirect('mind:detail', mind_map.id)

        form = NodeModelForm(self.request.POST)
        if form.is_valid():
            new_node = form.save(commit=False)
            new_node.parent = parent_node
            new_node.depth = parent_node.depth+1
            new_node.save()

        return redirect('mind:detail', mind_map.id)

    def put(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass








