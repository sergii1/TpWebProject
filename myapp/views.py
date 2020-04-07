from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib import auth
from . import models
from . import forms
from django.views.generic.edit import CreateView
from django.shortcuts import reverse


def index(request):
    template_name = 'index.html'
    authorised = False
    q = models.Question.objects.get_new()
    # q = [Question("title" + str(i), "text" + str(i), [1, 2, 3, 4], i) for i in range(6)]
    return render(request, template_name,
                  {'popularTags': ["perl", 'python', 'TechoPark', 'mysql', 'Django', 'mail.ru', 'bootstrap', 'html'],
                   'popularUsers': ['Mr.Freeman', 'Dr. House',
                                    'Bender', 'Queen Victoria', 'V. Pupkin'],
                   'pageList': [i for i in range(15)],
                   'questions': q,
                   'authorised': authorised
                   })


def ask(request):
    template_name = 'ask.html'
    return render(request, template_name,
                  {'popularTags': ["perl", 'python', 'TechoPark', 'mysql', 'Django', 'mail.ru', 'bootstrap', 'html'],
                   'popularUsers': ['Mr.Freeman', 'Dr. House',
                                    'Bender', 'Queen Victoria', 'V. Pupkin']
                   })


def login(request):
    print("login\n\n\n\n")
    if not request.POST:
        template_name = "login.html"
        return render(request, template_name,
                      {'popularTags': ["perl", 'python', 'TechoPark', 'mysql', 'Django', 'mail.ru', 'bootstrap',
                                       'html'],
                       'popularUsers': ['Mr.Freeman', 'Dr. House',
                                        'Bender', 'Queen Victoria', 'V. Pupkin']
                       })
    username = request.POST.get("username")
    password = request.POST.get("password")


def question(request, question_id):
    print("\n\n\n\n\nparam is", question_id)
    template_name = 'question.html'
    print("\n\n\n\n\n\n\n AAAAAAAAAAAAAAAAAAAAAAAAA")
    authorised = True
    # q = Question("title", "text", [1, 2, 3, 4], question_id)
    q = models.Question.objects.get(pk=question_id)
    answers = models.Question.objects.get_answers(question_id)

    print(q.title)
    return render(request, template_name,
                  {'popularTags': ["perl", 'python', 'TechoPark', 'mysql', 'Django', 'mail.ru', 'bootstrap', 'html'],
                   'popularUsers': ['Mr.Freeman', 'Dr. House',
                                    'Bender', 'Queen Victoria', 'V. Pupkin'],
                   'question': q,
                   'answers': answers,
                   'authorised': authorised,
                   })


def registration(request):
    template_name = 'registration.html'
    return render(request, template_name,
                  {'popularTags': ["perl", 'python', 'TechoPark', 'mysql', 'Django', 'mail.ru', 'bootstrap', 'html'],
                   'popularUsers': ['Mr.Freeman', 'Dr. House',
                                    'Bender', 'Queen Victoria', 'V. Pupkin'],

                   })


def tag(request, tag_name):
    template_name = 'tag.html'
    authorised = False
    q = models.Question.objects.get_tag(tag_name)

    return render(request, template_name,
                  {'popularTags': ["perl", 'python', 'TechoPark', 'mysql', 'Django', 'mail.ru', 'bootstrap', 'html'],
                   'popularUsers': ['Mr.Freeman', 'Dr. House',
                                    'Bender', 'Queen Victoria', 'V. Pupkin'],
                   'questions': q,
                   'answers': ['ans1', 'ans2', 'ans3'],
                   'tag': tag_name,
                   'pageList': [i for i in range(len(q))],
                   'authorised': authorised
                   })


def user_setting(request):
    template_name = 'userSetting.html'
    return render(request, template_name,
                  {'popularTags': ["perl", 'python', 'TechoPark', 'mysql', 'Django', 'mail.ru', 'bootstrap', 'html'],
                   'popularUsers': ['Mr.Freeman', 'Dr. House',
                                    'Bender', 'Queen Victoria', 'V. Pupkin'],

                   })


def hot(request):
    template_name = "index.html"
    authorised = False
    q = models.Question.objects.get_hot()
    return render(request, template_name,
                  {'popularTags': ["perl", 'python', 'TechoPark', 'mysql', 'Django', 'mail.ru', 'bootstrap', 'html'],
                   'popularUsers': ['Mr.Freeman', 'Dr. House',
                                    'Bender', 'Queen Victoria', 'V. Pupkin'],
                   'questions': q,
                   'authorised': authorised
                   })
