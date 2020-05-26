from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone


class QuestionManager(models.Manager):
    def get_hot(self):
        return self.order_by("-rating")

    def get_new(self):
        return self.order_by('-date')

    def get_tag(self, tag):
        return self.filter(tags__name=tag)

    def get_answers(self, question_pk):
        q = self.get(pk=question_pk)
        return Answer.objects.filter(question=q)

    def add_question(self, user, title, content, tags):
        author = Profile.objects.get(user=user)
        q = self.create(author=author, title=title, content=content, date=timezone.now(), rating=0)
        for tag in tags:
            t = Tag.objects.filter(name=tag)
            if t.count() != 0:
                t = t.first()
                t.rating += 1
                t.save()
            else:
                t = Tag.objects.create(name=tag)
                t.rating = 0
                t.save()
            q.tags.add(t)
        q.save()
        return q


class LikeManager(models.Manager):
    def create_like(self):
        pass


class ProfileManager(models.Manager):
    def get_top_users(self):
        return self.order_by("-rating")


class TagManager(models.Manager):
    def get_top_tags(self):
        return self.order_by("-rating")


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    nickname = models.CharField(max_length=100, unique=True)
    rating = models.IntegerField(default=0)
    objects = ProfileManager()

    def __str__(self):
        return self.nickname


class Question(models.Model):
    author = models.ForeignKey(Profile, blank=True, related_name="questions", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    title = models.TextField()
    content = models.TextField()
    tags = models.ManyToManyField("Tag")
    rating = models.IntegerField(default=0)
    objects = QuestionManager()
    likes = GenericRelation('Like', blank=True, related_query_name='question')

    def get_rating(self):
        res = 0
        for i in self.likes.all():
            res += i.value
        self.rating = res
        self.save(update_fields=["rating"])
        return res

    def get_absolute_url(self):
        return reverse("question", args=[self.pk])

    def __str__(self):
        return self.title


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    isCorrect = models.BooleanField(blank=True)
    rating = models.IntegerField(default=0)
    likes = GenericRelation('Like', related_query_name='answer')

    def get_rating(self):
        res = 0
        for i in self.likes.all():
            res += i.value
        self.rating = res
        self.save(update_fields=["rating"])
        return res


class Tag(models.Model):
    name = models.TextField()
    rating = models.IntegerField(default=0)
    objects = TagManager()

    def get_rating(self):
        res = Question.objects.filter(tags=self.name).count()
        self.rating = res
        self.save(update_fields=["rating"])
        return res

    def __str__(self):
        return self.name


class Like(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    VALUES = (("plus", 1), ("minus", -1))
    value = models.SmallIntegerField(choices=VALUES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
