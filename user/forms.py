from django import forms 
from .models import User 

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'roll',
            'department',
            'session',
            'phone_number',
            'address',
            'user_type',
            'image',
        ]
