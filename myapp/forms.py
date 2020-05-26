from django import forms
from . import models as md
from django.utils import timezone


class QuestionForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea())
    tags = forms.CharField(label="Tags", required=False)

    def clean_title(self):
        title = self.cleaned_data['title']
        print("\n\n\nclean data", title)
        if md.Question.objects.filter(title=title).count() != 0:
            print("AAAAAAAAAAAAAA")
            raise forms.ValidationError('This question already exist')
        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        return content

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if tags:
            tags = tags.split()
        return tags


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, min_length=3)
    password = forms.CharField(widget=forms.PasswordInput, min_length=4, max_length=50)


class AnswerForm(forms.Form):
    content = forms.CharField(label='Content', widget=forms.Textarea())

    def clean_body_answer(self):
        body_answer = self.cleaned_data['body_answer']
        return body_answer
