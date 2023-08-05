from django import forms
from .models import Question, Answer, Problem, Room, Message

from accounts.models import Account


# Question form
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('image', "title", "description", "tags")

    def save(self, commit=True):
        question = super().save(commit=False)

        if commit:
            question.save()

        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('image', "description")

    def save(self, commit=True):
        answer = super().save(commit=False)

        if commit:
            answer.save()

        return answer


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('title', "tags")

    def save(self, commit=True):
        problem = super().save(commit=False)

        if commit:
            problem.save()

        return problem


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['problem'] = forms.ModelChoiceField(queryset=Problem.objects.all())
        self.fields['user'] = forms.ModelChoiceField(queryset=Account.objects.all())
        self.fields['expert'] = forms.ModelChoiceField(queryset=Account.objects.all())

    def save(self, commit=True):
        room = super().save(commit=False)

        if commit:
            room.problem = self.cleaned_data['problem']
            room.user = self.cleaned_data['user']
            room.expert = self.cleaned_data['expert']
            room.assigned = True
            room.save()

        return room
