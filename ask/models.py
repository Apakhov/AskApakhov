from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist



class Profile(AbstractUser):
    upload = models.ImageField(upload_to='%Y/%m/%d/')

class Tag(models.Model):
    title = models.CharField(max_length=120, verbose_name=u"заголовок ярлыка")

    def __str__(self):
        return self.title

class QuestionManager(models.Manager):
    def order_by_date(self, amount):
        return super().order_by('-create_time')[:amount]
    
    def filter_by_tag(self, tag):
        try:
            return super().filter(tags__in=[Tag.objects.get(title=tag).id])
        except(ObjectDoesNotExist):
            return super().none()

    def order_by_hot(self):
        return super().order_by('-like_am')


class Question(models.Model):
    objects = QuestionManager()
    autor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name=u"заголовок ярлыка")
    tags = models.ManyToManyField(Tag, blank=True)
    text = models.CharField(max_length=10000, verbose_name=u"full text", default="i've got a problem")
    create_time = models.TimeField(auto_now_add=True)
    like_am = models.IntegerField(default=0,verbose_name=u"количество Лукашенко")

    def __str__(self):
        return self.title

class Answer(models.Model):
    autor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=10000, verbose_name=u"заголовок ярлыка")
    create_time = models.TimeField(auto_now_add=True)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    like_am = models.IntegerField(default=0,verbose_name=u"количество Лукашенко")
    def __str__(self):
        return self.text[:100]  

class Like(models.Model):
    autor = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )  

    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        null=True,
        default=None
    )