import random
from django.core.management.base import BaseCommand
from myapp.models import Question, User, Tag, Answer, Like, Profile
from faker import Faker

faker = Faker()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=0)
        parser.add_argument('--questions', type=int, default=0)
        parser.add_argument('--tags', type=int, default=0)

    def handle(self, *args, **options):
        tags = options['tags']
        users = options["users"]
        questions = options["questions"]

        print("users ", users)
        print("tags ", tags)
        print("questions ", questions)

        self.create_tags(tags)
        self.create_profiles(users)
        self.create_questions(questions)
        self.create_answers()
        self.create_likes()

    def create_tags(self, tags):
        for i in range(tags):
            tag = Tag.objects.create(name=faker.word() + str(i))
            tag.save()

    def create_profiles(self, users_amount):
        for i in range(users_amount):
            user = User.objects.create_user(faker.name() + str(i), faker.email(), '1234')
            user.save()
            p = Profile.objects.create(user=user)
            p.nickname = user.username
            p.save()

    def create_questions(self, number):

        authors = Profile.objects.all()
        tags = Tag.objects.all()
        for i in range(number):
            question = Question.objects.create(title=faker.sentence(),
                                               content=faker.text() + "?",
                                               author=random.choice(authors),
                                               rating=0)

            for j in range(3):
                tag = random.choice(tags)
                question.tags.add(tag)
                tag.rating += 1
                tag.save()
            question.save()

    def create_answers(self):
        if Answer.objects.count() > 0:
            return
        authors = Profile.objects.all()
        for question in Question.objects.all():
            for i in range(random.randint(1, 8)):
                a = Answer.objects.create(content=faker.text(), question=question, author=random.choice(authors),
                                          rating=0, isCorrect=True)
                a.save()

    def create_likes(self):
        authors = Profile.objects.all()
        for question in Question.objects.all():
            for i in range(random.randint(1, 5)):
                like = Like()
                like.value = 1
                like.author = random.choice(authors)
                like.content_object = question
                like.save()
            question.save()

        for answer in Answer.objects.all():
            for i in range(random.randint(1, 5)):
                like = Like()
                like.value = 1
                like.author = random.choice(authors)
                like.content_object = answer
                like.save()
            answer.save()
