from django import forms
from . models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','priority','category','completed','due_date']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control descrip'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            # 'completed': forms.BooleanField(attrs={'type': 'checkbox'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control'}),
        }
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m-%d-%Y'],
        label='Due Date'
    )
        

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'