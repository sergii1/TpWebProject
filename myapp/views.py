from django.shortcuts import render, redirect
from django.contrib import auth
from . import models
from . import forms
from django.core import paginator


def index(request):
    template_name = 'index.html'
    authorised = request.user.is_authenticated
    questions = models.Question.objects.get_new()

    pg = paginator.Paginator(questions, 5)  # По 2 на страницу
    page = request.GET.get('page')
    try:
        questions = pg.page(page)
    except paginator.PageNotAnInteger:
        # В случае, GET параметр не число
        questions = pg.page(1)
    except paginator.EmptyPage:
        questions = pg.page(pg.num_pages)

    user = None if not authorised else models.Profile.objects.get(user=request.user)

    return render(request, template_name,
                  {'popularTags': models.Tag.objects.get_top_tags()[0:10],
                   'popularUsers': models.Profile.objects.get_top_users()[0:10],
                   'questions': questions,
                   'authorised': authorised,
                   "user": user
                   })


def ask(request):
    if not request.user.is_authenticated:
        return redirect('login')

    template_name = 'ask.html'
    if request.method == 'GET':
        print(models.Profile.objects.get(user=request.user).id)
        question_form = forms.QuestionForm()
        return render(request, template_name,
                      {'popularTags': models.Tag.objects.get_top_tags()[0:10],
                       'popularUsers': models.Profile.objects.get_top_users()[0:10],
                       'form': question_form,
                       "authorised": True,
                       "user": models.Profile.objects.get(user=request.user)
                       })

    form = forms.QuestionForm(request.POST)
    # print("\n\n\n eeeeeeeeeeeeeeeeeeeers", form.cleaned_data['title'], form.cleaned_data['content'],
    #       form.cleaned_data['tags'])
    print("\n\nVALID", str(request.POST.get("title")))

    if form.is_valid():
        q = models.Question.objects.add_question(user=request.user, title=form.cleaned_data['title'],
                                                 content=form.cleaned_data['content'],
                                                 tags=form.cleaned_data['tags'])

        print("\n\n\nIS VALId")
        return redirect('question', question_id=q.id)

    return render(request, template_name,
                  {'popularTags': models.Tag.objects.get_top_tags()[0:10],
                   'popularUsers': models.Profile.objects.get_top_users()[0:10],
                   'form': form,
                   "authorised": True,
                   "user": models.Profile.objects.get(user=request.user)
                   })


def login(request):
    template_name = "login.html"
    if not request.POST:
        form = forms.LoginForm()
        return render(request, template_name,
                      {'popularTags': models.Tag.objects.get_top_tags()[0:10],
                       'popularUsers': models.Profile.objects.get_top_users()[0:10],
                       "form": form,
                       }
                      )
    form = forms.LoginForm(request.POST)
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return redirect("index")

    return render(request, template_name,
                  {'popularTags': models.Tag.objects.get_top_tags()[0:10],
                   'popularUsers': models.Profile.objects.get_top_users()[0:10],
                   'errortext': "Неправильный логин или пароль",
                   "form": form,
                   }
                  )


def logout(request):
    auth.logout(request)
    return redirect("index")


def question(request, question_id):
    template_name = 'question.html'
    form = forms.AnswerForm()
    if not request.POST:
        authorised = request.user.is_authenticated
        q = models.Question.objects.get(pk=question_id)
        answers = models.Question.objects.get_answers(question_id)
        return render(request, template_name,
                      {'popularTags': models.Tag.objects.get_top_tags()[0:10],
                       'popularUsers': models.Profile.objects.get_top_users()[0:10],
                       'question': q,
                       'answers': answers,
                       'authorised': authorised,
                       "user": None if not authorised else models.Profile.objects.get(user=request.user),
                       'form': form
                       })
    form = forms.AnswerForm(request.POST)
    if form.is_valid():
        answer = models.Answer.objects.create(author=models.Profile.objects.get(user=request.user),
                                              question=models.Question.objects.get(pk=question_id),
                                              content=form.cleaned_data['content'], isCorrect=True)
        answer.save()
    return redirect('question', question_id)


def registration(request):
    template_name = 'registration.html'
    return render(request, template_name,
                  {'popularTags': models.Tag.objects.get_top_tags()[0:10],
                   'popularUsers': models.Profile.objects.get_top_users()[0:10],

                   })


def tag(request, tag_name):
    template_name = 'tag.html'
    authorised = request.user.is_authenticated
    q = models.Question.objects.get_tag(tag_name)

    return render(request, template_name,
                  {'popularTags': models.Tag.objects.get_top_tags()[0:10],
                   'popularUsers': models.Profile.objects.get_top_users()[0:10],
                   'questions': q,
                   'answers': ['ans1', 'ans2', 'ans3'],
                   'tag': tag_name,
                   'authorised': authorised,
                   "user": None if not authorised else models.Profile.objects.get(user=request.user)
                   })


def user_setting(request):
    if not request.user.is_authenticated:
        return redirect("login")

    template_name = 'userSetting.html'
    return render(request, template_name,
                  {'popularTags': models.Tag.objects.get_top_tags()[0:10],
                   'popularUsers': models.Profile.objects.get_top_users()[0:10],
                   "user": models.Profile.objects.get(user=request.user)

                   })


def hot(request):
    template_name = "index.html"
    authorised = request.user.is_authenticated
    questions = models.Question.objects.get_hot()
    pg = paginator.Paginator(questions, 5)  # По 2 на страницу
    # tags = models.Tag.objects.best_tags()[0:10]
    # users = Client.objects.best_members()[0:10]
    page = request.GET.get('page')
    try:
        questions = pg.page(page)
    except paginator.PageNotAnInteger:
        # В случае, GET параметр не число
        questions = pg.page(1)
    except paginator.EmptyPage:
        questions = pg.page(pg.num_pages)
    return render(request, template_name,
                  {'popularTags': models.Tag.objects.get_top_tags()[0:10],
                   'popularUsers': models.Profile.objects.get_top_users()[0:10],
                   'questions': questions,
                   'authorised': authorised,
                   "user": None if not authorised else models.Profile.objects.get(user=request.user)

                   })
