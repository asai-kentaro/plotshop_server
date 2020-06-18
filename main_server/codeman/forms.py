from django import forms
from .models import CodeElement


class CodeElementForm(forms.ModelForm):
    class Meta:
        model = CodeElement
        fields = (
            "title", "code"
        )
