from django.contrib import admin
from .models import Question, QuestionCounts, Answer, AnswerCounts, Vote, Problem, Room, Message


# Question admin
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'last_modified', 'account', 'image', "title", "description", "tags")
    search_fields = ('id', 'created', 'last_modified', "title", "description")
    readonly_fields = ('id', 'created', 'last_modified')
    ordering = ('id', 'created', 'last_modified')


admin.site.register(Question, QuestionAdmin)


# Question Count admin
class QuestionCountsAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'last_modified', "votes_count", "display_voted_by", "views_count")
    search_fields = ('id', 'created', 'last_modified')
    readonly_fields = ('id', 'created', 'last_modified')
    ordering = ('id', 'created', 'last_modified', "votes_count", "views_count")

    def display_voted_by(self, obj):
        return ", ".join([str(account.id) for account in obj.voted_by.all()])

    display_voted_by.short_description = 'Voted By'


admin.site.register(QuestionCounts, QuestionCountsAdmin)


# Question admin
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'last_modified', 'account', 'question', "image", "description")
    search_fields = ('id', 'created', 'last_modified', "description")
    readonly_fields = ('id', 'created', 'last_modified')
    ordering = ('id', 'created', 'last_modified')


admin.site.register(Answer, AnswerAdmin)


# Answer Count admin
class AnswerCountsAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'last_modified', "answer", "votes_count", "display_voted_by")
    search_fields = ('id', 'created', 'last_modified')
    readonly_fields = ('id', 'created', 'last_modified')
    ordering = ('id', 'created', 'last_modified', "votes_count")

    def display_voted_by(self, obj):
        return ", ".join([str(account.id) for account in obj.voted_by.all()])

    display_voted_by.short_description = 'Voted By'


admin.site.register(AnswerCounts, AnswerCountsAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'last_modified', "account", "question_vote", "answer_vote", "upvote")
    search_fields = ('id', 'created', 'last_modified')
    readonly_fields = ('id', 'created', 'last_modified')
    ordering = ('id', 'created', 'last_modified')


admin.site.register(Vote, VoteAdmin)


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'last_modified', "account", "title", "tags")
    search_fields = ('id', 'created', 'last_modified')
    readonly_fields = ('id', 'created', 'last_modified')
    ordering = ('id', 'created', 'last_modified')


admin.site.register(Problem, ProblemAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'last_modified', "problem", "user", "expert", "ai", "assigned")
    search_fields = ('id', 'created', 'last_modified')
    readonly_fields = ('id', 'created', 'last_modified')
    ordering = ('id', 'created', 'last_modified')


admin.site.register(Room, RoomAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'room', "account", "image", "content")
    search_fields = ('id', 'timestamp', 'content')
    readonly_fields = ('id', 'timestamp')
    ordering = ('id', 'timestamp')


admin.site.register(Message, MessageAdmin)
