import random
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from myapp.models import Question as Poll
from myapp.models import Question, User, Tag, Answer, QuestionLike, Profile
from faker import Faker
import myapp.models as Md
from random import randint

faker = Faker()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=0)
        parser.add_argument('--questions', type=int, default=0)
        parser.add_argument('--number', type=int, default=1)

    def handle(self, *args, **options):
        number = options['number']

        self.create_tags()
        self.create_profiles()
        self.create_questions(number)
        self.create_answers()
        self.create_likes()

    def create_tags(self):
        if Tag.objects.count() > 8:
            return

        for i in range(5):
            tag = Tag.objects.create(name=faker.word() + str(i))
            tag.save()

    def create_profiles(self):
        if User.objects.count() > 8:
            return
        for i in range(8):
            user = User.objects.create_user(faker.name()+str(i), faker.email(), '1234')
            user.save()
            p = Profile.objects.create(user=user)
            p.nickname = user.username
            p.save()

    def create_questions(self, number):

        authors = Md.Profile.objects.all()
        tags = Tag.objects.all()
        for i in range(number):
            question = Question.objects.create(title=faker.sentence(),
                                               content=faker.text(),
                                               author=random.choice(authors),
                                               rating=0)

            for j in range(3):
                tag = random.choice(tags)
                question.tags.add(tag)
            question.save()

    def create_answers(self):
        if Answer.objects.count() > 0:
            return
        authors = Md.Profile.objects.all()
        for question in Question.objects.all():
            for i in range(random.randint(1, 8)):
                a = Answer.objects.create(content=faker.text(), question=question, author=random.choice(authors),
                                          rating=0, isCorrect=True)

                a.save()

    def create_likes(self):
        authors = Md.Profile.objects.all()
        for question in Question.objects.all():
            for i in range(random.randint(1, 5)):
                like = Md.QuestionLike()
                like.value = 1
                like.author = random.choice(authors)
                like.question = question
                like.save()
            question.save()

        for answer in Md.Answer.objects.all():
            for i in range(random.randint(1, 5)):
                like = Md.AnswerLike()
                like.value = 1
                like.author = random.choice(authors)
                like.answer = answer
                like.save()
            answer.save()
