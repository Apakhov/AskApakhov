from django import forms

from ask.models import Question


class QuestionForm(forms.ModelForm):
    tags = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'long'})

    def clean_tags(self):
        tags_str = self.cleaned_data.get('tags')
        tags = [tag.strip() for tag in tags_str.split(',') if tag]

        if len(tags):
            raise forms.ValidationError("Need tags")

        return tags

    class Meta:
        model = Question
        exclude = ['autor', 'like_am']