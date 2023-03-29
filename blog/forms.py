from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    image_link = forms.CharField(max_length=1255, required=False) # 이미지 링크 입력 필드

    class Meta:
        model = Post
        fields = ['title', 'content', 'image_link']
