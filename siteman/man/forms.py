from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Man, Wife, Category


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label='Категория')
    wife = forms.ModelChoiceField(queryset=Wife.objects.all(), required=False, empty_label="Не женат", label='Жена')

    class Meta:
        model = Man
        fields = ['title', 'content', 'photo', 'is_published', 'cat', 'wife', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символом')

        return title


class UploadFilesForm(forms.Form):
    file = forms.ImageField(label='Фото')
