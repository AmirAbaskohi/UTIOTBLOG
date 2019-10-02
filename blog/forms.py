from django import forms
from .models import Post
from .choices import *

class CreatePostForm(forms.ModelForm):
	title = forms.CharField(max_length=100)
	content = forms.CharField(widget=forms.Textarea)
	category = forms.ChoiceField(choices=CATEGORIES,widget=forms.Select(),required=True)

	class Meta:
		model = Post
		fields = ['title','content','category']