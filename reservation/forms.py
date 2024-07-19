from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    doctor_id = forms.IntegerField(required=True)

    class Meta:
        model = Comment
        fields = ["title", "text", "score"]
