
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


def recursive_data(instance):
    a = {'title': instance.node.title, 'content': instance.node.content, 'depth': instance.node.depth, 'id': instance.node.id}
    children = []
    for node in instance.children:
        children.append(recursive_data(node))
    a['children'] = children
    return a

