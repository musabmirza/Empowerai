from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Job
from .models import  Application



class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'skills_required', 'salary']
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser

# class SignupForm(UserCreationForm):
#     role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

# class Meta:
#     model = CustomUser
#     fields = ['username', 'email', 'role', 'password1', 'password2']
class SignupForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']  # FIXED
        if commit:
            user.save()
        return user


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'skills_required', 'salary']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows':4, 'placeholder':'Write a short cover letter (optional)'}),
        }
