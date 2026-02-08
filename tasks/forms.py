from django import forms
from .models import Task
from django.utils import timezone

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(),
            'description': forms.Textarea(attrs={'rows':4}),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        if deadline < timezone.now().date():
            raise forms.ValidationError("Дедлайн не может быть в прошлом")
        return deadline

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 10:
            raise forms.ValidationError("Описание должно быть минимум 10 символов")
        return description
