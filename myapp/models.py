from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse


class QuestionManager(models.Manager):
    def get_hot(self):
        return self.order_by("-rating")

    def get_new(self):
        return self.order_by('date')

    def get_tag(self, tag):
        return self.filter(tags__name=tag)

    def get_answers(self, question_pk):
        q = self.get(pk=question_pk)
        return Answer.objects.filter(question=q)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    nickname = models.CharField(max_length=100, unique=True)
    rating = models.IntegerField(default=0)


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    title = models.TextField()
    content = models.TextField()
    tags = models.ManyToManyField("Tag", related_name="questions", related_query_name="question")
    rating = models.IntegerField(default=0)
    objects = QuestionManager()

    def get_absolute_url(self):
        return reverse("question", args=[self.pk])


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    isCorrect = models.BooleanField(blank=True)
    rating = models.IntegerField(default=0)


class Tag(models.Model):
    name = models.TextField()


class AnswerLike(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    VALUES = (("plus", 1), ("minus", -1))
    value = models.SmallIntegerField(choices=VALUES)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.answer.rating += self.value
        print("new answer rating is ", self.answer.rating)
        self.answer.save()
        self.author.rating += self.value
        print("new author rating is ", self.author.rating)
        self.author.save()


class QuestionLike(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    VALUES = (("plus", 1), ("minus", -1))
    value = models.SmallIntegerField(choices=VALUES)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.question.rating += self.value
        print("new question rating is ", self.question.rating)
        self.question.save()
        self.author.rating += self.value
        print("new author rating is ", self.author.rating)
        self.author.save()
