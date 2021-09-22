from django import forms
from .models import MindMap, Node


class MindMapModelForm(forms.ModelForm):

    class Meta:
        model = MindMap
        fields = ['root_node']


class NodeModelForm(forms.ModelForm):

    class Meta:
        model = Node
        fields = ['title', 'content']

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'content': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            )
        }
