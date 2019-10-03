from django import forms
from ckeditor.fields import RichTextFormField

class ArticleForm(forms.Form):
    content = RichTextFormField()

