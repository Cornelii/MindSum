from django.db import models

# Create your models here.


class NodeManager(models.Manager):
    def create_node(self, title, content, depth):
        node = self.create(title=title, content=content, depth=depth)

        return node


class Node(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    depth = models.IntegerField()
    parent = models.ForeignKey('Node', on_delete=models.CASCADE, related_name='children', null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = NodeManager()


class MindMap(models.Model):
    root_node = models.OneToOneField('Node', on_delete=models.CASCADE, related_name='mind_map')
    max_depth = models.IntegerField(default=5)



