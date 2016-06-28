from django import forms
from .models import Post
from .models import Question

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'text',)

class ContactForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ('name', 'question',)