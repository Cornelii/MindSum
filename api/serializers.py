from rest_framework import serializers
from mind.models import Node, MindMap


class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Node
        fields = '__all__'


class MindMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = MindMap
        fields = '__all__'


class TreeSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return self.recursive_data(instance)


    def recursive_data(self, instance):
        a = {'title':instance.node.title, 'content':instance.node.content, 'depth':instance.node.depth, 'id':instance.node.id}
        children = []
        for node in instance.children:
            children.append(self.recursive_data(node))
        a['children'] = children
        return a

    def create(self, validated_data):
        pass

    def data(self):
        pass

    def is_valid(self, raise_exception=False):
        pass

    def validated_data(self):
        pass

    def errors(self):
        pass

    def save(self, **kwargs):
        pass

