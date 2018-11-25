from django import forms

from ask.models import Question, Profile
from django.core.validators import validate_email


class QuestionForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Why are we stil here? Just to suffer?'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Every night, I can feel my leg… and my arm… even my fingers. The body I’ve lost… the comrades I’ve lost… won’t stop hurting… It’s like they’re all still there. You feel it, too, don’t you?'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'tag1, tag2, tag3...'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_tags(self):
        tags_str = self.cleaned_data.get('tags')
        tags = [tag.strip() for tag in tags_str.split(',') if tag]
        print("TAGS:", tags)
        if len(tags) == 0:
            raise forms.ValidationError("Need tags")

        if len(tags) > 3:
            raise forms.ValidationError("Need 1 to 3 tags")

        return tags

    class Meta:
        model = Question
        exclude = ['autor', 'like_am', 'is_active']

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Sergey'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'serega666@bmstu.ru'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Vampir666'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    upload = forms.ImageField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
   

    def clean_email(self):
        validate_email(self.cleaned_data.get("email"))

    def clean(self):
        password = self.cleaned_data.get("password")
        repeat_password = self.cleaned_data.get("repeat_password")
        if password != repeat_password:
            raise forms.ValidationError("Passwords are different")

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = Profile
        fields = ['first_name','email','username','password', 'upload']