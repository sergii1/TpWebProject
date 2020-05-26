from django.contrib import admin

from . import models


# Register your models here.


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Like)
class AnswerAdmin(admin.ModelAdmin):
    pass

# @admin.register(models.AnswerLike)
# class AnswerLikeAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(models.QuestionLike)
# class QuestionLikeAdmin(admin.ModelAdmin):
#     pass
