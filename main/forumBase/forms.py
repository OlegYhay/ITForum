import django.forms as forms

from forumBase.models import CommentTopic


class ModelComment(forms.ModelForm):
    CommentText= forms.CharField(widget=forms.Textarea(attrs={'cols': 5, 'rows': 3}),label='Комментарий')
    class Meta:
        model = CommentTopic
        fields = ['CommentText']