from django import forms

from notesworks.models import Task

from django. contrib. auth.models import User

class TaskForm(forms.ModelForm):

    class Meta:

        model=Task

        
        #fields="__all__"

        exclude=("created_date","status","user")

        widgets={
            
            "title":forms.TextInput(attrs={"class":"form-control",'style': 'background-color: #f0f8ff;'}),

            "description":forms.Textarea(attrs={"class":"form-control",'style': 'background-color: #f0f8ff;'}),

            "due_date":forms.DateInput(attrs={"class":"form-control","type":"date",'style': 'background-color: #f0f8ff;'}),

            "category":forms.Select(attrs={"class":"form-control form-select",'style': 'background-color: #f0f8ff;'}),
            
            "user":forms.TextInput(attrs={"class":"form-control",'style': 'background-color: #f0f8ff;'})
                                           

        }


class RegistrationForm(forms.ModelForm):

    class Meta:

        model=User

        fields=["username","email","password"]

        widgets={
            "password":forms.PasswordInput()
        }

class SignInForm(forms.Form):

    username=forms.CharField()

    password=forms.CharField(widget=forms.PasswordInput())
