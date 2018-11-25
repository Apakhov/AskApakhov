from django.contrib import admin

# Register your models here.
from ask.models import Profile, Question, Tag, Answer, Like 

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Answer)